```plantuml
@startuml
skinparam linetype ortho
sample_table --|> child1
sample_table --|> child2
sample_table --|> child3
child1 --|> child4
child2 --|> child5
@enduml