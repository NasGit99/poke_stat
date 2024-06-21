
resource "aws_ecs_cluster" "cluster" {
  name = "pokestat_cluster"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }
}

# Allow Ecs instances to assume the role
data "aws_iam_policy_document" "ecs_assume_role_policy" {
  statement {
    actions = [
      "sts:AssumeRole"
    ]
    effect = "Allow"
    principals {
      type        = "Service"
      identifiers = ["ecs.amazonaws.com"]
    }

  }
}

# Create the policy which allows other actions for the EC2 instance
data "aws_iam_policy_document" "ecs_domain_join_policy" {
  statement {
    actions = [
                "ecr:BatchGetImage",
                "ecr:GetDownloadUrlForLayer",
                "ecr:GetAuthorizationToken"
    ]
    effect = "Allow"
    resources = ["*"]
  }
}

resource "aws_iam_role" "ecs_join_role" {
  name               = "ecs-domain-join-policy"
  assume_role_policy = data.aws_iam_policy_document.ecs_assume_role_policy.json
 
  # Attach the policy
  inline_policy {
    policy = data.aws_iam_policy_document.ecs_domain_join_policy.json
  }
}

resource "aws_iam_role_policy" "ecs_join_role" {
  name = "iam_policy"
  role = aws_iam_role.ecs_join_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        "Action": [
                "ecr:BatchGetImage",
                "ecr:GetDownloadUrlForLayer",
                "ecr:GetAuthorizationToken"
            ,
        ]
        Effect   = "Allow"
        Resource = "*"
      },
    ]
  })
}



resource "aws_ecs_task_definition" "service" {

  family                   = "ecs-task-definition-demo"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  memory                   = "1024"
  cpu                      = "512"
  execution_role_arn       = "arn:aws:iam::${data.aws_caller_identity.account.account_id}:role/ecsTaskExecutionRole"
  container_definitions    = <<EOF
[
  {
    "name": "demo-container",
    "image": "${data.aws_caller_identity.account.account_id}.dkr.ecr.us-east-1.amazonaws.com/pokestat:latest",
    "memory": 1024,
    "cpu": 512,
    "essential": true,
    "entryPoint": ["/"],
    "portMappings": [
      {
        "containerPort": 80,
        "hostPort": 80
      }
    ]
  }
]
EOF
}



resource "aws_ecs_service" "pokestat" {
  name            = "pokestat_service"
  cluster         = aws_ecs_cluster.cluster.id
  task_definition = aws_ecs_task_definition.service.arn
  desired_count   = 1
  launch_type     = "FARGATE"
  network_configuration {
    subnets          = ["subnet-092483ab9a578867f"]
    assign_public_ip = true
  }
#  iam_role        = aws_iam_role.ecs_join_role.arn 
  depends_on      = [aws_iam_role_policy.ecs_join_role]



 
}