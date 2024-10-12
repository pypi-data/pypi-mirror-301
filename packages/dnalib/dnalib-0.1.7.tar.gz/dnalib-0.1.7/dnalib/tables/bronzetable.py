from dnalib.utils import Utils, LandingZoneUtils, TableUtils
from dnalib.custom import YamlLoader
from dnalib.log import *
from dnalib.core import CreateTableBronze
from dnalib.writer import WriteModes
from .tables import LayerTable
from enum import Enum
from pyspark.sql.functions import from_utc_timestamp, current_timestamp, concat, col, row_number, when
from delta.tables import DeltaTable
from pyspark.sql.window import Window
import yaml

class SourceType(Enum):
    """ 
        Enum que define os métodos validos para origem de dados: TXT, CSV, PARQUET, KAFKA e EVENTHUB (WIP); SQLSERVER, ORACLE (implementados).
    """
    TXT = "txt"
    CSV = "csv"
    PARQUET = "parquet"    
    KAFKA = "kafka"
    EVENTHUB = "eventhub"
    SQLSERVER = "sqlserver"
    ORACLE = "oracle"

class LandingLoader(Enum):
    """ 
        Enum que define a forma como os dados serão carregados a partir da origem: 
        INCREMENTAL: considera que a origem é um arquivo incremental e define automaticamente que será feito um upsert.
        FULL: considera que a origem é um arquivo completo, e define automaticamente que será feito um overwrite.
        CDC: considera que a origem é um arquivo CDC (funciona somente para SourceType.SQLSERVER) e define automaticamente que será feito um upsert.
        STREAMING: WIP.
    """
    INCREMENTAL = "incremental" # read a single part, and merge data
    FULL = "full" # read all, then overwrite    
    CDC = "cdc" # only for cdc loader    
    STREAMING = "streaming" # for streaming purpose

class FileLandingLoader:
    """
        A classe FileLandingLoader é uma implementação de alto nível que define a carga de um arquivo da landing zone (todas ingestões batch são baseadas em arquivos
        seja csv, txt ou banco, que nesse último caso usa parquet).

        Args:
            landing_files_path (str): caminho na landingzone de onde o arquivo será lido.
            table_name (str): string que representa o nome da tabela.          
            loader_type (LandingLoader): algum dos tipos válidos da LandingLoader.            
            name_filter (str, optional): utilizado caso seja necessário filtrar arquivos dentro de um mesmo diretório da landing.

        Attributes:
            landing_files_path (str): caminho na landingzone de onde o arquivo será lido.
            table_name (str): string que representa o nome da tabela.    
            loader_type (LandingLoader): algum dos tipos válidos da LandingLoader.            
            name_filter (str, optional): utilizado caso seja necessário filtrar arquivos dentro de um mesmo diretório da landing.

    """
    def __init__(self, 
                 landing_files_path, 
                 table_name,
                 loader_type,                 
                 name_filter = ""):
        self.landing_files_path = landing_files_path
        self.table_name = table_name
        self.loader_type = loader_type        
        self.name_filter = name_filter
        self.df_landing = None

    def load_incremental(self):
        # TODO: implementar o load do tipo incremental. (deve retornar um DataFrame Spark)
        raise NotImplementedError("Method load_incremental() must be implemented.")

    def load_full(self):
        # TODO: implementar o load do tipo full. (deve retornar um DataFrame Spark)
        raise NotImplementedError("Method load_full() must be implemented.")

    def load_cdc(self):
        # TODO: implementar o load do tipo cdc. (deve retornar um DataFrame Spark)
        raise NotImplementedError("Method load_cdc() must be implemented.")    

    def load(self):
        if self.loader_type.value == LandingLoader.INCREMENTAL.value:
            self.df_landing = self.load_incremental()
        elif self.loader_type.value == LandingLoader.FULL.value:
            self.df_landing = self.load_full()
        elif self.loader_type.value == LandingLoader.CDC.value:
            self.df_landing = self.load_cdc()
        else:
            log(__name__).error(f"Invalid load type {self.loader_type}")
            raise ValueError(f"Invalid load type {self.loader_type}")
        log(__name__).info(f"Load of {self.loader_type.value} type for {self.table_name} completed successfully.")
        return self

class SqlParquetLandingLoader(FileLandingLoader):

    # This implementation is based on adf:
        # table/date/ -> incremental path
        # table/date/ -> cdc path
        # table/date/ -> full path = if process run in incremental mode, but you specified a full query
        # table/ -> full path
    
    def __init__(self, landing_files_path, table_name, loader_type, table_config):
        super().__init__(landing_files_path, table_name, loader_type) 
        self.spark = Utils.spark_instance()  # Obtém a instância do Spark usando Utils.spark_instance()                        
        self.table_config = table_config

    def load_df_parquet(self):
        # le o path mais recente dentro da pasta indicada por landing_files_path
        file_path = LandingZoneUtils.load_last_updated_path(self.landing_files_path)
        # Lê os dados do parquet atual
        try:
            df = self.spark.read.parquet(file_path) 
        except Exception as e:
            log(__name__).error(f"Error reading parquet file: {e}")          
            raise Exception(f"Error reading parquet file: {e}")
        return df

    def load_incremental(self):       
        return self.load_df_parquet()

    def load_full(self):
        return self.load_df_parquet()
        
class SqlServerParquetLandingLoader(SqlParquetLandingLoader):

    # only applied in cdc purposes
    cdc_metadata_columns = ["LAST_UPDATE", "start_lsn", "end_lsn", "seqval", "operation", "update_mask", "command_id", "data_alteracao"]

    def __init__(self, landing_files_path, table_name, loader_type, table_config):
        super().__init__(landing_files_path, table_name, loader_type, table_config)

    def load_cdc(self):
        df = self.load_incremental()                

        # query que pega a última alteração de cada registro
        df = (df.withColumnRenamed("__$start_lsn", "start_lsn") 
               .withColumnRenamed("__$end_lsn", "end_lsn") 
               .withColumnRenamed("__$seqval", "seqval") 
               .withColumnRenamed("__$operation", "operation") 
               .withColumnRenamed("__$update_mask", "update_mask") 
               .withColumnRenamed("__$command_id", "command_id"))
        
        # view para filtrar as alterações
        df.createOrReplaceTempView("vw_table_logs")
        self.spark.sql(f"""
            CREATE OR REPLACE TEMP VIEW vw_table_logs_rownumber AS (
                SELECT * FROM (
                    SELECT 
                        *, 
                        ROW_NUMBER() OVER(PARTITION BY {self.table_config['key']} ORDER BY data_alteracao DESC, command_id DESC) AS LAST_UPDATE FROM vw_table_logs
                    WHERE operation <> 3                                                
                )
                WHERE LAST_UPDATE = 1
            );
        """)

        # filtra as operações de insert e update
        df_upinsert = self.spark.sql(""" 
            SELECT * 
            FROM vw_table_logs_rownumber 
            WHERE operation IN (2, 3, 4);
            """).drop(*self.cdc_metadata_columns)                      
        return df_upinsert        

class OracleParquetLandingLoader(SqlParquetLandingLoader):

    def __init__(self, landing_files_path, table_name, loader_type, table_sufix, table_config):
        super().__init__(landing_files_path, table_name, loader_type, table_sufix, table_config)

class FileLoaderFactory:
    @staticmethod
    def create_file_loader(source_type, landing_files_path, table_name, loader_type, table_config):
        if source_type.value == SourceType.SQLSERVER.value:
            return SqlServerParquetLandingLoader(landing_files_path, table_name, loader_type, table_config)
        elif source_type.value == SourceType.ORACLE.value:
            return OracleParquetLandingLoader(landing_files_path, table_name, loader_type, table_config)
        else:
            log(__name__).error(f"file_loader could not be created for source_type {source_type}")
            raise ValueError(f"file_loader could not be created for source_type {source_type}")
        
class BronzeTable(LayerTable):

    layer = "bronze"

    def __init__(self,                  
                 table_name,                 
                 landing_files_path,                                   
                 yaml_config_path,
                 table_sufix = "",
                 source_type=SourceType.SQLSERVER, 
                 loader_type=LandingLoader.FULL,
                 source_df=None, 
                 name_filter="", 
                 unzip=True, 
                 include_checksum=False):
        super().__init__(self.layer, f"{table_sufix}_{table_name}", source_df, include_checksum)        
        self.landing_files_path = landing_files_path
        self.name_filter = name_filter
        self.table_sufix = table_sufix
        self.source_type = source_type
        self.yaml_config_path = yaml_config_path
        self.table_config = Utils.yaml_table_parameters(table_name=f"{table_sufix}_{table_name}", yml_file_path=yaml_config_path)
        self.loader_type = loader_type
        self.unzip = unzip        
        self.except_fields = {}

        # Usa a fábrica para criar o file_loader correto
        self.file_loader = FileLoaderFactory.create_file_loader(
            self.source_type,
            self.landing_files_path,
            self.table_name,
            self.loader_type,            
            self.table_config
        )        

    def parse_df_source(self):
        """
            Método que executa o carregamento de dados da camada landing para a bronze

            Returns:
                source_df (spark DataFrame): dataframe carregado a partir da camada source, caso source_df seja None.

        """         
        # load strategy in this case is to check if the table exists        
        return self.file_loader.load().df_landing

    def load_fields_from_source(self):                
        return "*"
    
    def create_table(self, yml={}, partition_fields=[], tbl_properties={}, replace=False):
        if not self.has_loaded:
            self.load()
            log(__name__).warning(f"The load() method will be called internally because you call create_table first.") 
        self.creat_tbl = CreateTableBronze(self.target_df.schema, self.table_name, yml, partition_fields, tbl_properties, replace).execute()
        return self
    
    # implementar lógica usando mode = None (nesse caso a decisão usa o LandingLoader como parâmetro caso contrário fica a critério de quem escolheu)
    def persist(self, mode=WriteModes.OVERWRITE, partition_fields=[], optimize=True, source_df_name="source", update_df_name="update", merge_condition=None):        
        has_delete = False                
        # when you have cdc ingestion, you may need to upsert
        if self.loader_type.value == LandingLoader.CDC.value:
            mode = WriteModes.UPSERT
            merge_condition = self.table_config["merge"]
            has_delete = True        
        elif self.loader_type.value == LandingLoader.INCREMENTAL.value:
            mode = WriteModes.UPSERT
            merge_condition = self.table_config["merge"]        

        # calling super persist method
        super().persist(mode=mode, partition_fields=partition_fields, optimize=optimize, source_df_name=source_df_name, update_df_name=update_df_name, merge_condition=merge_condition)

        # only for cdc purposes
        if has_delete:            
            key_columns = ",".join(self.table_config["key"]) if isinstance(self.table_config["key"], list) else self.table_config["key"]
            delete_condition = f"SELECT concat({key_columns}) FROM vw_table_logs_rownumber WHERE operation = 1"
            self.writer.delete(key_columns, delete_condition)       
        return self     

