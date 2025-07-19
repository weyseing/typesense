# ECR Setup
- **Create ECR repository.**

![image](assets/1.PNG)

- **Build & upload to ECR**
    - Ensure env below are set **.env**
        - `AWS_ACCOUNT_ID`
        - `AWS_REGION`
        - `AWS_ACCESS_KEY_ID`
        - `AWS_SECRET_ACCESS_KEY`
        - `AWS_ECR`
    - Run `cli/deploy_ecr.sh`

# ECS Setup
- **Create ECS cluster**

![image](assets/2.PNG)

- **Create Task Definition**

![image](assets/3a.PNG)
![image](assets/3b.PNG)
![image](assets/3c.PNG)

- **Create ECS Service**

![image](assets/4.PNG)
![image](assets/5.PNG)

# EXEC into ECS Task
- **Create Task Role**
    - **\*\*MUST\*\* add `AmazonSSMManagedInstanceCore` policy**

![image](assets/6.PNG)
![image](assets/12.PNG)
![image](assets/7.PNG)

- Update **Task Role** in **Task Definition**

![image](assets/8.PNG)

- **\*\*MUST\*\* redeploy new ECS Task (via new Task Definition)** to reflect Task Role

![image](assets/11.PNG)

- Ensure variable below are set in **cli/ecs_set_exec.sh**
    - `REGION`
    - `CLUSTER_ARN`
    - `SERVICE_ARN`

- Run `cli/ecs_set_exec.sh` to **turn ON EXEC Settings**

![image](assets/9.PNG)

- Check **EXEC Settings** is ON.

![image](assets/10.PNG)

- **\*\*MUST\*\* redeploy new ECS Task (via Force New Deploy)** to reflect EXEC Settings

![image](assets/14.PNG)

- Ensure variable below are set in **cli/ecs_ssh.sh** to enter ECS Task.
    - `REGION`
    - `CLUSTER_ARN`

- Run `cli/ecs_ssh.sh <YOUR TASK ID>`

![image](assets/13.PNG)

# ALB Setup
- **Create Target Group**

![image](assets/15.PNG)
![image](assets/16.PNG)
![image](assets/17.PNG)

- **Create ALB**

![image](assets/18.PNG)
![image](assets/19.PNG)
![image](assets/20.PNG)
![image](assets/21.PNG)

- **Update ECS**

![image](assets/22.PNG)
![image](assets/23.PNG)
![image](assets/24.PNG)

- **Wait Target to be spinned up**

![image](assets/25.PNG)

- **Test via LB DNS**

![image](assets/26.PNG)
![image](assets/27.PNG)
