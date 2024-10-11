package com.databricks.labs.remorph.intermediate

trait UnwantedInGeneratorInput

case class UnresolvedRelation(inputText: String) extends LeafNode with UnwantedInGeneratorInput {
  override def output: Seq[Attribute] = Seq.empty
}

case class UnresolvedExpression(inputText: String) extends LeafExpression with UnwantedInGeneratorInput {
  override def dataType: DataType = UnresolvedType
}

case class UnresolvedAttribute(unparsed_identifier: String, plan_id: Long = 0, is_metadata_column: Boolean = false)
    extends LeafExpression {
  override def dataType: DataType = UnresolvedType
}

case class UnresolvedFunction(
    function_name: String,
    arguments: Seq[Expression],
    is_distinct: Boolean,
    is_user_defined_function: Boolean,
    has_incorrect_argc: Boolean = false)
    extends Expression {
  override def children: Seq[Expression] = arguments
  override def dataType: DataType = UnresolvedType
}

case class UnresolvedStar(unparsed_target: String) extends LeafExpression {
  override def dataType: DataType = UnresolvedType
}

case class UnresolvedRegex(col_name: String, plan_id: Long) extends LeafExpression {
  override def dataType: DataType = UnresolvedType
}

case class UnresolvedExtractValue(child: Expression, extraction: Expression) extends Expression {
  override def children: Seq[Expression] = child :: extraction :: Nil
  override def dataType: DataType = UnresolvedType
}

case class UnresolvedCommand(inputText: String) extends Catalog with Command with UnwantedInGeneratorInput {
  override def output: Seq[Attribute] = Seq.empty
  override def children: Seq[LogicalPlan] = Seq.empty
}

case class UnresolvedCatalog(inputText: String) extends Catalog with UnwantedInGeneratorInput {
  override def output: Seq[Attribute] = Seq.empty
  override def children: Seq[LogicalPlan] = Seq.empty
}

case class UnresolvedCTAS(inputText: String) extends Catalog with Command with UnwantedInGeneratorInput {
  override def output: Seq[Attribute] = Seq.empty
  override def children: Seq[LogicalPlan] = Seq.empty
}

case class UnresolvedModification(inputText: String) extends Modification with UnwantedInGeneratorInput {
  override def output: Seq[Attribute] = Seq.empty
  override def children: Seq[LogicalPlan] = Seq.empty
}
