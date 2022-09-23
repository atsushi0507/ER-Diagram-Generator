import sys
sys.path.append("../")
from ER_diagram_generator import ERDiagram

writer = ERDiagram("Sample Diagram")

out_name = "test.md"

writer.make_entity("test", None, None)
writer.make_entity("Projects", "project_id", None)
writer.make_entity("Models", "model_id", "project_id")
writer.make_entity("Experiments", "experiment_id", "model_id")
writer.make_entity("Experiments2", ["exp_id", "project_id"])

writer.output_table(out_name)
