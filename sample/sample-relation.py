import sys
sys.path.append("../")
from ER_diagram_generator import ERDiagram

writer = ERDiagram("Sample Diagram")

out_name = "test-relation.md"

load_file = "../tables/test.md"
writer.load_table(load_file)

writer.make_relation("Models", "Experiments", 4)
writer.make_relation("Projects", "Models", 4)
writer.make_relation("Projects", "Experiments2")

writer.output_relation(out_name)