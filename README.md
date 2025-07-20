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

# EFS Setup
- **Create File System**

![image](assets/28.PNG)
![image](assets/29.PNG)

- **Create Access Point**

![image](assets/30.PNG)
![image](assets/31.PNG)
![image](assets/38.PNG)

- **Security Group inbound & outbound**
    - `EFS security group`: Allow port 2049 in **Inbound**
    - `ECS security group`: Allow port 2049 in **Outbound**

![image](assets/32.PNG)

- **Add IAM Policy to Task Role**

![image](assets/35.PNG)
![image](assets/36.PNG)

- **Set EFS File System Policy**

```json
{
    "Version": "2012-10-17",
    "Id": "EFSFileAccessPolicy",
    "Statement": [
        {
            "Sid": "AllowAccessFromECSThroughAccessPoint",
            "Effect": "Allow",
            // update Task Role ARN
            "Principal": {
                "AWS": "arn:aws:iam::107698500998:role/ecs-typesense-task-role"
            },
            "Action": [
                "elasticfilesystem:ClientMount",
                "elasticfilesystem:ClientWrite"
            ],
            // update EFS ARN
            "Resource": "arn:aws:elasticfilesystem:ap-southeast-1:107698500998:file-system/fs-0aee593c9e02bcbd9",
            "Condition": {
                "StringEquals": {
                    // update EFS access point ARN
                    "elasticfilesystem:AccessPointArn": "arn:aws:elasticfilesystem:ap-southeast-1:107698500998:access-point/fsap-0205b099f7a40eb07"
                }
            }
        }
    ]
}
```

- **Set EFS Volume in ECS Task Definition**

![image](assets/33.PNG)
![image](assets/34.PNG)
![image](assets/37.PNG)

- **Deploy NEW ECS task**

# Check EFS Folder (via EC2)
