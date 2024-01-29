
resource "aws_ecs_cluster" "cluster" {
  name = "pokestat_cluster"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }
}

resource "aws_ecs_task_definition" "service" {
  family = "service"
  
  container_definitions = jsonencode([
    {
      name      = "pokestat"
      image     = "${data.aws_caller_identity.account.account_id}.dkr.ecr.us-east-1.amazonaws.com/pokestat:latest"
      cpu       = 1
      memory    = 512
      essential = true
      portMappings = [
        {
          containerPort = 80
          hostPort      = 80
        }
      ]
    },
  ])

  volume {
    name      = "service-storage"
    host_path = "/ecs/service-storage"
  }

}

resource "aws_ecs_service" "pokestat" {
  name            = "pokestat_service"
  cluster         = aws_ecs_cluster.cluster.id
  task_definition = aws_ecs_task_definition.service.arn
  desired_count   = 1



  ordered_placement_strategy {
    type  = "binpack"
    field = "cpu"
  }


 
}