resource "aws_lambda_function" "lambda" {
  filename      = "lambda.zip" # Nome do arquivo zip contendo seu código Node.js
  function_name = var.lambda_name
  role          = aws_iam_role.lambda_role.arn
  handler       = "index.handler"
  runtime       = "nodejs20.x"

  source_code_hash = data.archive_file.zip.output_base64sha256

  environment {
    variables = var.env_vars
  }

  depends_on = [aws_iam_role.lambda_role]
}

data "archive_file" "zip" {
  type        = "zip"
  source_dir  = "${path.module}/../app"
  output_path = "${path.module}/lambda.zip"
}
