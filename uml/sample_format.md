```plantuml
@startuml
title Sample Diagram
entity sample_table{
+ column_0 [PK]
+ column_2 [PK]
+ column_5 [PK]
--
column_1 [FK]
column_3 [FK]
}
entity child1{
+ column_1 [PK]
--
column_3 [FK]
}
entity child2{
+ column_0 [PK]
+ column_1 [PK]
--
column_3 [FK]
}
entity child3{
+ column_0 [PK]
--
column_4 [FK]
}
entity child4{
+ column_0 [PK]
+ column_1 [PK]
+ column_3 [PK]
--
column_3 [FK]
}
entity child5{
+ column_0 [PK]
+ column_1 [PK]
--
column_3 [FK]
}
@enduml