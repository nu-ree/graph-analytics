# Databricks notebook source
# DBTITLE 1,Chapter 6. Working with Different Types of Data
# 6장의 구성 내용
# |-- Booleans - done!
# |-- Numbers - done!
# |-- Strings - done! 
# |-- Dates and timestamps
# |-- Handling Null  - done! 
# |-- Complex Types  - done! 
# |-- User-defined Functions - done! 

# COMMAND ----------

# DBTITLE 1,Intro
# Spark의 transformation functions는 계속 발전하고 있기 때문에 최신 자료를 참고하는것이 좋음
# Spark의 methods는 크게 두 가지로 나눌 수 있음 : 
    # - DataFrame(Dataset) methods : Dataframe은 Dataset의 `Row` type임. 데이터 로우 단에 적용하는 methods. (예: `DataFrameStatFunctions`,`DataFrameNaFunctions` )
    # - Column methods :  칼럼에 대한 function (예 : `alias` & `contains`) ==> ch5에서 많이 다룸

# COMMAND ----------

# 데이터 불러오기
# File location and type
file_location = "/FileStore/tables/2010_12_01-ec65d.csv"
file_type = "csv"

# CSV options
infer_schema = "true"
first_row_is_header = "true"
delimiter = ","

# The applied options are for CSV files. For other file types, these will be ignored.
df = spark.read.format(file_type) \
  .option("inferSchema", infer_schema) \
  .option("header", first_row_is_header) \
  .option("sep", delimiter) \
  .load(file_location)

# COMMAND ----------

df.createOrReplaceTempView("dfTable") # df에 불러놓은 데이터를 가지고 dfTable라는 이름의 뷰를 만들어줌 --> 나중에 SQL 문으로 쿼리 가능
df.printSchema()

# COMMAND ----------

# DBTITLE 1,(1) Converting to Spark Types : 'lit' 
# 스파크에서 데이터를 다루기 위해서는 native type을 Spark types로 바꿔주는 것이 안전함
# lit : 다른 언어에서 쓰이는 data types를 그에 상응하는 Spark type으로 바꿔줌
from pyspark.sql.functions import lit, expr 
df.select(lit(5), lit("five"), lit(5.0))  #lit은 literals의 약자 

# COMMAND ----------

df.select(expr("*"), lit(1).alias("one")).show(2) # 숫자1을 'one'이라는 이름의 칼럼을 만들어서 붙여주세요.

# COMMAND ----------

# MAGIC %sql
# MAGIC # -- SQL문법으로는
# MAGIC SELECT * , 1 as one FROM dfTable limit 2

# COMMAND ----------

# DBTITLE 1,(2) Working with booleans
#1 ) where 절에서 != , == , <> 로 필터링
from pyspark.sql.functions import col
df.where(col("InvoiceNo") != 536365)\
.select("InvoiceNo", "Description")\
.show(5, False)

# COMMAND ----------

# df.where("InvoiceNo = 536365").show(5, False)
df.where("Quantity <> 6").show(5, False) # <>는 !=랑 같은 개념. 

# COMMAND ----------

# 2. or / and로 boolean statement 묶어주기 (# | , & 이용)
# Spark는 모든 filtering 조건문을 하나의 statement로 동등하게 보고 flatten 하여 알아서 최적화된 순서 만들어줌, 동시에 실행 
from pyspark.sql.functions import instr
# -- 방법 1: boolen expression 사용하기
priceFilter = col("UnitPrice") > 600
descripFilter = instr(df.Description, "POSTAGE") >=1
df.where(col("StockCode").isin("DOT")).where(priceFilter & descripFilter).show() # 첫번째where와 두번째 where는 and로 붙음! 

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *, StockCode in ("DOT") AND (UnitPrice > 600 OR instr(Description, "POSTAGE")>=1) as isExpensive
# MAGIC FROM dfTable WHERE StockCode in ("DOT") AND (UnitPrice > 600 OR instr(Description, "POSTAGE")>=1)

# COMMAND ----------

# -- 방법 2 : Boolen 칼럼 만들기 
DOTCodeFilter = col("StockCode") == 'DOT'
priceFilter = col("UnitPrice")>600
descripFilter = instr(col("Description"), "POSTAGE") >= 1

df.withColumn("isExpensive", DOTCodeFilter & (priceFilter|descripFilter)).where('isExpensive').select("unitPrice", "isExpensive").show(5)

# COMMAND ----------

# 3. 칼럼을 만들때, boolean expression이 아니라 SQL statement를 활용할 수도 있음!
from pyspark.sql.functions import expr
a.withColumn("isExpensive", expr("NOT Unitprice <= 250")).where("isExpensive").select("isExpensive","Description", "UnitPrice").show(5)

# COMMAND ----------

# 그런데 테스트할 데이터에 Null이 있다면? 결과로 나오는 데이터의 길이가 다를 수 있음. eqNullSafe쓰자. Equality test that is safe for null values.
df.where(col("Description").eqNullaSafe("WHITE METAL LANTERN")).show(2, False)
# df.where(col("Description")!="Hello").show(2, False)

# COMMAND ----------

# 그런데 데이터에 Null이 있다면? x eqNullSafe : Equality test that is safe for null values.
df.where(col("Description").eqNullSafe("Hello")).show()

# COMMAND ----------



# COMMAND ----------

# DBTITLE 1,(3) Working with Numbers! (power / round/ bround / correlation / describe / approxQuantile / crosstab / monoid)
# 1) Power
from pyspark.sql.functions import expr, pow, col
fabricatedQuantity = pow(col("Quantity")*col("UnitPrice"), 2)  + 5# Returns the value of the first argument raised to the power of the second argument.
df.select(expr("CustomerId"), fabricatedQuantity.alias("realQuantity")).show(2)

# COMMAND ----------

# selectExpr 을 사용해서 SQL 스타일로 쓸 수도 있음!
df.selectExpr("CustomerId", "(POWER((Quantity * UnitPrice), 2.0)+5) as realQuantity").show(2)

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT customerId, (POWER((Quantity*UnitPrice),2)+5) as realQuantity FROM dfTable Limit 2

# COMMAND ----------

# 2) Rounding
from pyspark.sql.functions import lit, round, bround
df.select(round(lit(2.3)), bround(lit("2.5"))).show(1)

# COMMAND ----------

# 3) correlaton 
from pyspark.sql.functions import corr
df.stat.corr("Quantity", "UnitPrice")
df.select(corr("Quantity", "UnitPrice")).show()

# COMMAND ----------

# 4) describe(mean, count, sd, min, max)
from pyspark.sql.functions import count, mean, stddev_pop, min, max

df.describe().show()

# COMMAND ----------

# 5) Approximate quantiles
# >> The result of this algorithm has the following deterministic bound: If the DataFrame has N elements and if we request the quantile at probability p up to error err, then the algorithm will return a sample x from the DataFrame so that the *exact* rank of x is close to (p * N). More precisely,
# floor((p - err) * N) <= rank(x) <= ceil((p + err) * N).
# This method implements a variation of the Greenwald-Khanna algorithm (with some speed optimizations). The algorithm was first present in Space-efficient Online Computation of Quantile Summaries by Greenwald and Khanna.

colName = "UnitPrice"
quantileProbs = [0.25]
relError = 0.05
df.stat.approxQuantile("UnitPrice", quantileProbs, relError)
# 위 셀의 unitPirice의 describe를 보면 0~607.9까지 데이터가 분포해있음을 알 수 있음
# quantileProbs = 0.5로 설정했으므로, 데이터를 작은 수부터 큰수 순으로 나열했을 때 중간쯤(o.5 +- 0.05  즉 0.45~0.55)에 있는 UnitPrice가 얼마인지 알려준다. 
# 평균치는 4.15임에 비해 대략적인 중위값은 2.51이므로 왼쪽으로 치우친 형태임을 짐작할 수 있다. 

# COMMAND ----------

# 6) Crosstab
df.stat.crosstab("StockCode", "Quantity").show(2)
# df.stat.freqItems(["StockCode", "Quantity"]).show()

# COMMAND ----------

# 7) monotonically_increasing_id
# add a unique ID to each row
from pyspark.sql.functions import monotonically_increasing_id
df.select(monotonically_increasing_id(),col("StockCode")).show(2)
# df.select(monotonically_increasing_id().alias('ID')).show(2)

# COMMAND ----------

# 그 외 random data 생성하는 rand(), randn() 등 새로운 statfunctions 많이 개발중!
# bloom filtering, sketching algo 등 advanced tasks를 다룰 수 있는 function도. 
# >블룸 필터는 원소가 집합에 속하는지 여부를 검사하는데 사용되는 확률적 자료 구조
# > sketching algorithms : https://en.wikipedia.org/wiki/Streaming_algorithm

# COMMAND ----------

# DBTITLE 1,(4) Working with String(initcap / upper / lower, lpad / ltrim / rpad / rtrim / trim)
from pyspark.sql.functions import initcap, lower, upper
# df.select(initcap(col("Description"))).show(2)
df.select(col("Description"), initcap(col("Description")), lower(col("Description")), upper(lower(col("Description")))).show(2) # caplitalized

# COMMAND ----------

# MAGIC %sql
# MAGIC --in sql
# MAGIC SELECT initcap(Description), lower(Description), upper(Description) FROM dfTable LIMIT 2

# COMMAND ----------

from pyspark.sql.functions import lit, ltrim, rtrim, rpad, lpad, trim
df.select(lit(" HELLO ").alias('normal'),
ltrim(lit("  HELLO ")).alias("ltrim"), # 왼쪽 여백 지우기
rtrim(lit(" HELLO ")).alias("rtrim"), # 오른쪽 여백 지우기
trim(lit(" H E L L O ")).alias("trim"), # 양쪽 여백 지우기
# strip(lit(" H E L L O ")).alias("strip"), 
lpad(lit(" HELLO"), 3, " ").alias("lp3"), # 빈칸 포함 왼쪽에서부터 3자로 만들기          
lpad(lit(" HELLO"), 10, "^").alias("lp10"), # 빈칸 포함 왼쪽에서부터 10자로 만들기. 남는칸은 "."로 채우기
rpad(lit("HELLO"), 10, "_").alias("rp")).show(2) # 오른쪽부터 총 10칸남기고, 빈칸은 " "

# COMMAND ----------

# MAGIC %sql
# MAGIC -- in SQL
# MAGIC SELECT
# MAGIC ltrim(' HELLLOOOO '),
# MAGIC rtrim(' HELLLOOOO '),
# MAGIC trim(' HELLLOOOO '),
# MAGIC lpad('HELLOOOO ', 3, ' '),
# MAGIC rpad('HELLOOOO ', 10, ' ')
# MAGIC FROM dfTable

# COMMAND ----------

# DBTITLE 1,(5) Regular Expressions (regexp_extract, regexp_replace, translate, contains)
# Spark의 regex 는 Java의 regex의 장점을 따옴 (?)
# 크게 regexp_extract, regexp_replace로 나눌 수 있음

# COMMAND ----------

# 1) regexp_replace : regex에 해당하는 string을 xx로 대체
from pyspark.sql.functions import regexp_replace
regex_string = "BLACK|WHITE|RED|GREEN|BLUE"
df.select(col("Description").alias("Original_description"), 
regexp_replace(col("Description"), regex_string, "COLOR").alias("color_clean")).show(2)

# COMMAND ----------

# MAGIC %sql
# MAGIC -- in SQL
# MAGIC SELECT
# MAGIC regexp_replace(Description, 'BLACK|WHITE|RED|GREEN|BLUE', 'COLOR') as
# MAGIC color_clean, Description
# MAGIC FROM dfTable

# COMMAND ----------

# 2) Translate : indexed character를 특정 character로 바꾸기
from pyspark.sql.functions import translate
df.select(translate(col("Description"), "LEET", "1337"), translate(col("Description"), "HAVING", "...."), col("Description")).show(2)
# L --> 1, E -->3, E--->3, T ---> 7
# H, A, V, I, N, G ---> .

# COMMAND ----------

# MAGIC %sql
# MAGIC -- in SQL
# MAGIC SELECT Description, translate(Description, 'LEET', '1337'), translate(Description, '-', '?!') FROM dfTable

# COMMAND ----------

# 3) regexp_extract : regex에 매치되는 n번째 단어 가져오기 
from pyspark.sql.functions import regexp_extract
extract_str = "(BLACK|WHITE|RED|GREEN|BLUE|METAL)"
df.select(
regexp_extract(col("Description"), extract_str, 0).alias("color_clean"),
#   regexp_extract(col("Description"), extract_str).alias("color_clean_noindex"),
# regexp_extract(col("Description"), extract_str, 2).alias("metal"), # index error @@@@@????? 왜이랩..
col("Description")).show(2, False)

#https://people.apache.org/~pwendell/spark-nightly/spark-master-docs/latest/api/sql/index.html

# COMMAND ----------

# 4) contains (=instr)
# 특정 string을 가지는지 여부를 boolean 값으로 얻기
# case 1: 조건이 적은 경우
from pyspark.sql.functions import instr
containsBlack = instr(col("Description"), "BLACK") >= 1
containsWhite = instr(col("Description"), "WHITE") >= 1

df.withColumn("hasSimpleColor", containsBlack | containsWhite)\
.where("hasSimpleColor")\
.select("Description").show(3, False)

# COMMAND ----------

# %sql
# SELECT Description FROM dfTable
# WHERE instr(Description, 'BLACK') >= 1 OR instr(Description, 'WHITE') >= 1

# COMMAND ----------

# case2. 조건이 여러개가 되는 경우 (locate 사용)
# --> Spark accepts dynamic numbsers of arguments
from pyspark.sql.functions import expr, locate
simpleColors = ["black", "white", "red", "green", "blue"]

# 해당 단어가 위치한 자리 찾기
def color_locator(column, color_string):
  return locate(color_string.upper(), column).cast("boolean").alias("is_" + color_string) #책에 오타다~~~~~~~ 

# COMMAND ----------

selectedColumns = [color_locator(df.Description, c) for c in simpleColors]
selectedColumns

# COMMAND ----------

type(selectedColumns)

# COMMAND ----------

selectedColumns.append(expr("*")) # has to a be Column type
selectedColumns

# COMMAND ----------

# select 문 안에 list 형식으로 구문을 넣음
# df.select(*selectedColumns).where(expr("is_white OR is_red")).select("Description").show(3, False)
df.select(*selectedColumns).where(expr("is_white OR is_red")).show(3, False)

# COMMAND ----------



# COMMAND ----------

# DBTITLE 1,(6) Working with Timestapms


# COMMAND ----------

# DBTITLE 1,(7) Working with Nulls in Data (coalesce / ifnull, nullif, nvl, nvl2 / drop / fill / replace / ordering) 
# Null: missing or empty data in DataFrame
# > "being explicit is always better than implicit"
# 'null이 없는 칼럼'이라고 define을 해도 null값을 넣을 수 있음. 이러한 "nullable signal"은 단지 SQL 쿼리 옵티마이제이션을 위한 것일 뿐!
# Null 값을 핸들링하는 2가지 방법
# 1) explicitly drop nulls
# 2) fill with a value

# COMMAND ----------

# 1) Coalsce : 
# 참고: Repartition에서 사용했던 coalesce(지난주) 
# Coalesce, on the other hand, will not incur a full shuffle and will try to combine partitions. This
# operation will shuffle your data into five partitions based on the destination country name, and
# then coalesce them (without a full shuffle):
df.repartition(5, col("Country")).coalesce(2) # 5개로 나누고 2개로 합치기 (?)

# COMMAND ----------

# 또는 여기서 나오는 것처럼 columns set에 대해서 null값 제외한 first non-null values 레코드 반환에 사용 
from pyspark.sql.functions import coalesce
df.select(col("Description"), col("CustomerId"), coalesce(col("Description"), col("CustomerId"))).filter(df['CustomerId'].isNull()).show(10, False) # 여기는 null 값이 없어서 그냥 show(3) 하는 것과 결과 같음

# COMMAND ----------

# 또는 여기서 나오는 것처럼 columns set에 대해서 null값 제외한 first non-null values 레코드 반환에 사용 
from pyspark.sql.functions import coalesce
df.select(col("Description"), col("CustomerId"), coalesce(col("Description"), col("CustomerId"))).show(10, False) # 여기는 null 값이 없어서 그냥 show(3) 하는 것과 결과 같음

# COMMAND ----------

# MAGIC %sql
# MAGIC -- 2) ifnull, nullif, nvl, nvl2 (in SQL)
# MAGIC SELECT
# MAGIC ifnull(null, 'return_value'), -- 왼쪽값이 null 이면 오른쪽값 반환
# MAGIC nvl(null, 'return_value'), -- 동일
# MAGIC 
# MAGIC ifnull('null anim', 'return_value'), -- 왼쪽값이 null이 아니면 원래값 그대로 반환
# MAGIC nvl('null anim', 'return_value'), -- 동일
# MAGIC 
# MAGIC nullif('value', 'value'), -- 왼쪽값이 오른쪽 값이면 null 반환
# MAGIC nullif('value', 'va'), -- 왼쪽값이 오른쪽 값이 아니면 원래값 그대로 반환
# MAGIC 
# MAGIC nvl2('not_null', 'return_value', "else_value"), -- 1번 값이 null 이 아니면 2번반환 아니면 3번 반환 
# MAGIC nvl2(null, 'return_value', "else_value") -- 1번 값이 null 이 아니면 2번반환 아니면 3번 반환 
# MAGIC FROM dfTable LIMIT 1

# COMMAND ----------

# 3) drop : 
df.na.drop() # default = any. null값 하나라도 있는 로우 버리기
# df.na.drop('any') 
# df.na.drop('all') # 로우 전체가 null이면 버리기
# df.na.drop('all', subset=['StockCode', 'InvoiceNo']) #특정 칼럼에 대해서만

# COMMAND ----------

# 4) fill:
# df.na.fill("All Null values become this string")
# df.na.fill(5:Integer) # type이 integer인 칼럼만 골라서 5로 채워넣기
# df.na.fill("all", subset=["StockCode", "InvoiceNo"]) # 특정 칼럼에 대해서 공통된 값 채워넣기 
 
fill_cols_vals = {"StockCode": 5, "Description" : "No Value"} # 칼럼마다 원하는 값 채워넣기 
df.na.fill(fill_cols_vals)

# COMMAND ----------

# 5) replace : null이건 뭐건 원하는 값으로 바꾸기 (단 해당 칼럼의 type과 맞는 값으로만 가능)
df.na.replace([""], ["UNKNOWN"], "Description")

# COMMAND ----------

# 6) ordering : asc_nulls_first, desc_nulls_first, asc_nulls_last, or desc_nulls_last

# COMMAND ----------

# DBTITLE 1,(8) Working with Complex Types(structs, arrays, maps)
# help you *organize* & *structure* your data!
# 1) Structs : DataFrames within DataFrames
from pyspark.sql.functions import struct
complexDF = df.select(struct("Description", "InvoiceNo").alias("complex"))
complexDF.createOrReplaceTempView("complexDF")
complexDF.show(2 ,False )
# complexDF.select("complex.*").show(2) # complexDF 안에 있는 complex 칼럼의 df 꺼내보기

# complex 칼럼 안에 들어있는 dataframe에서 칼럼 description을 가져오려면? . 혹은 description 이용!
# complexDF.select(col("complex").getField("Description")).show(2) 
complexDF.select("complex.InvoiceNo").show(2, False)

# COMMAND ----------

# MAGIC %sql
# MAGIC -- in SQL
# MAGIC SELECT complex.* FROM complexDF limit 2

# COMMAND ----------

# 2) Arrays
# use case : Descriptoin 칼럼에 있는 단어들을 가져와서 DataFrme의 row로 만들기 (새로운 칼럼?!)

# part 1: split
from pyspark.sql.functions import split
# df.select(split(col("Description"), " ")).show(2)
df.select(split(col("Description"), " ").alias("array_col")).selectExpr("array_col[0]").show(2)
# df.select(split(col("Description"), " ").alias("array_col")).show(100)
df.select(col("Description")).show(10)
from pyspark.sql.functions import size
df.select(size(split(col("Description"), " "))).show(2) # shows 5 and 3


from pyspark.sql.functions import array_contains 
df.select(array_contains(split(col("Description"), " "), "WHITE")).show(2)

# COMMAND ----------

# part 2: explode
# To convert a complex type into a set of rows(one per value in our array), we need to use the explode function.
from pyspark.sql.functions import split, explode
df.withColumn("splitted", split(col("Description"), " "))\
.withColumn("exploded", explode(col("splitted")))\
.select("Description", "InvoiceNo", "exploded").show(20, False)

# COMMAND ----------

# MAGIC %sql
# MAGIC -- 1. split
# MAGIC SELECT split(Description, ' ') FROM dfTable limit 4

# COMMAND ----------

# MAGIC %sql
# MAGIC -- 2. explode
# MAGIC SELECT Description, InvoiceNo, exploded
# MAGIC FROM (SELECT *, split(Description, " ") as splitted FROM dfTable)
# MAGIC LATERAL VIEW explode(splitted) as exploded 
# MAGIC LIMIT 5

# COMMAND ----------

# 3) Maps : key-value pairs of columns
from pyspark.sql.functions import create_map
df.select(create_map(col("Description"), col("InvoiceNo")).alias("complex_map")).show(2, False)

# COMMAND ----------

# MAGIC %sql
# MAGIC -- in SQL
# MAGIC SELECT map(Description, InvoiceNo) as complex_map FROM dfTable
# MAGIC WHERE Description IS NOT NULL LIMIT 5

# COMMAND ----------

df.select(create_map(col("Description"), col("InvoiceNo")).alias("complex_map")).show(2, False)

# COMMAND ----------

df.select(create_map(col("Description"), col("InvoiceNo")).alias("complex_map")).selectExpr("complex_map['WHITE METAL LANTERN']").show(2) # key가 없으면 null값 반환 ..

# COMMAND ----------

df.select(create_map(col("Description"), col("InvoiceNo")).alias("complex_map"))\
.selectExpr("explode(complex_map)").show(2, False)

# COMMAND ----------

# DBTITLE 1,(9) Working with JSON
jsonDF = spark.range(1).selectExpr(""" '{"myJSONKey" : {"myJSONValue" : [1, 2, 3]}}' as jsonString""")
jsonDF.show(2, False)

# COMMAND ----------

from pyspark.sql.functions import get_json_object, json_tuple, to_json, from_json
jsonDF.select(
# get_json_object(col("jsonString"), "$.myJSONKey.myJSONValue[1]") as "column",
get_json_object(col("jsonString"), "$.myJSONKey.myJSONValue[1]").alias("column"), 
json_tuple(col("jsonString"), "myJSONKey")).show(2, False)

# COMMAND ----------

jsonDF

# COMMAND ----------

# MAGIC %sql
# MAGIC jsonDF.selectExpr("json_tuple(jsonString, '$.myJSONKey.myJSONValue[1]') as column").show(2)

# COMMAND ----------

from pyspark.sql.functions import from_json
from pyspark.sql.types import *
parseSchema = StructType((
StructField("InvoiceNo",StringType(),True),
StructField("Description",StringType(),True)))

# COMMAND ----------

df.selectExpr("(InvoiceNo, Description) as myStruct")\
.select(to_json(col("myStruct")).alias("newJSON"))\
.select(from_json(col("newJSON"), parseSchema), col("newJSON")).show(2)

# COMMAND ----------

# DBTITLE 1,(10) User-Defined Functions
# 하나 혹은 그 이상의 칼럼을 인풋값으로 받고 아웃풋값으로 낼 수 있음
# 어떤 언어로도 쓸 수 있음. 퍼포먼스는 다를 수 있음. 
  # Scala or Java : 퍼포먼스 패널티 x. but 다른 기존의 builtin functions 못씀. JVM에서 사용. objects를 많이 쓰면 퍼포먼스 이슈 있을 수 있음 --> ch 19에서 옵티마이제이션 다룸
  # Python : Spark가 worker에 python process를 시작함. 
        #파이썬이 이해할 수 있는 형태로 변환 데이터를 serialize 함(?) --> python process에 function execute --> JVM and Spark에 return result
        # python process를 실행하는 것은 costly 함
            # - 1)computation 자체가 비쌈
            # - 2)데이터를 파이썬 프로세스로 보내버리고 나면, 워커의 메모리를 스파크가 관리할 수 없음 ==> 리소스 부족으로 worker가 fail할지도. (JVM이랑 python이랑 같은 리소스를 공유하니까)

  # Scala나 Java로 UDF 쓸 것을 권장 
# operate on data, record by record

# COMMAND ----------

def square_float(x):
    return float(x**2)
square_udf_float2 = udf(lambda z: square_float(z), FloatType())

# COMMAND ----------

# temporary in a specific SparkSession (or context) --> 여러머신에서 쓰고 싶으면 register 해야함(?)
udfExampleDF = spark.range(5).toDF("num")
def power3(double_value):
  return double_value ** 3
power3(2.0) #"input must be a specific type and cannot be a null value"

from pyspark.sql.functions import udf
power3udf = udf(power3)

from pyspark.sql.functions import col
udfExampleDF.select(power3udf(col("num"))).show(2)
