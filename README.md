# Setup
- Copy `.env.exmple` to `.env.`
- Set **ENV value** below
    - `TYPESENSE_ENDPOINT`: This is `localhost:8108` for local and LB IP for prod.
- **Up the container with** `docker compose up -d`

# ECR Setup
- **Create ECR repository.**

![image](assets/1.PNG)

- **Build & upload to ECR**
    - Ensure env below are set **.env**
        - `AWS_ACCOUNT_ID`
        - `AWS_DEFAULT_REGION`
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

- **Set EFS Volume in ECS Task Definition**

![image](assets/33.PNG)
![image](assets/34.PNG)
![image](assets/37.PNG)

- **Deploy NEW ECS task**

# Check EFS Folder (via EC2)

- **Create EC2 instance**

![image](assets/39.PNG)
![image](assets/40.PNG)
![image](assets/41.PNG)
![image](assets/42.PNG)

- **\*\*MUST\*\*** allow `PORT 2049` in **Security Group**

- **Change SSH key permission**
    - `sudo chmod 400 ssh-key-2.pem`

- **SSH inside to EC2**
    - `ssh -i "ssh-key-2.pem" admin@ec2-13-215-156-78.ap-southeast-1.compute.amazonaws.com`

- **Setup amazon-efs-utils** 
    - Install dependencies
        ```shell
        sudo apt-get update
        sudo apt-get install -y git make libssl-dev build-essential curl pkg-config nfs-common stunnel4
        ```

    - Install Rush & Cargo
        ```shell
        curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
        source "$HOME/.cargo/env"
        ```

    - Install amazon-efs-utils
        ```shell
        cd ~
        git clone https://github.com/aws/efs-utils.git
        cd efs-utils
        ./build-deb.sh
        ls -l ./build/ # Find the exact .deb filename
        ```

        ```shell
        sudo dpkg -i ./build/amazon-efs-utils-<YOUR_VERSION>_amd64.deb # Use the exact filename found
        sudo apt-get install -f
        ```

- **Mount to EFS**
    ```shell
    sudo mount -t efs -o tls <YOUR EFS ID>:/ <YOUR MOUNT PATH>
    sudo mount -t efs -o tls fs-*****************:/ /mnt/efs
    ```

- **Check EFS ID & mount path**
    ```
    ps aux | grep -i stunnel | grep -i <YOUR EFS ID> --color=auto
    ps aux | grep -i stunnel | grep -i fs-************ --color=auto
    ```

![image](assets/43.PNG)