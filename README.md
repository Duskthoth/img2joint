# Melfa Img2Joint Controller

#### Projeto desenvolvido na disciplina de Projeto Integrador I 🎓

Trabalho apresentado para o componente curricular Projeto Integrador I, com o intuito de gerar um programa para controle de um manipulador robótico Melfa RV-4FRM-D através da utilização da biblioteca OpenCV e ROS.



## Equipe:

<ul>
<li>Andrew de Carvalho Dellamea</li>
<li>Brendha Iara Gruber de Lima</li>
<li>Felipe Alves Santana</li>
<li>Matheus Ernan Reichert</li>
</ul>

## Projetos de Referência 💾

Os seguintes projetos foram utilizados como base para realização deste trabalho:

📷 Openni camera project : Disponível [aqui](https://github.com/ros-drivers/openni_camera)

🦾 Melfa_robot: Disponível [aqui](https://github.com/tork-a/melfa_robot)

🎱 Ball_tracker and ROS: Disponível [aqui](https://github.com/trunc8/ball-tracking-opencv-and-ros)

## Dependências do pacote 💻

Para utilizar o pacote deste repositorio, é necessário realizar o passo a passo presente no [site]([kinetic/Installation/Ubuntu - ROS Wiki](http://wiki.ros.org/kinetic/Installation/Ubuntu)) oficial do ROS Kinetic-Kame e em seguida instalar as dependências necessárias.

As seguintes dependências devem ser instaladas no sistema Ubuntu 16.04 ou semelhante:

```bash
sudo apt install ros-kinetic-desktop-full ros-kinetic-melfa-robot \
ros-kinetic-openni-camera ros-kinetic-openni-launch
```

Em seguida deve-se criar um pacote catkin da seguinte forma:

```bash
mkdir -p catkin_ws/src
cd catkin_ws/
catkin_make
cd src/
git clone https://github.com/Duskthoth/melfa_img2joint.git
cd ..
catkin_make
```

Abra o arquivo .bashrc e adicione a seguinte linha ao fim do arquivo

```bash
source /opt/ros/kinetic/setup.sh
```

## Executando o programa 💽

Para iniciar o programa cada linha a seguir deve ser rodada em um terminal diferente na seguinte ordem:

Inicia o Driver do kinect

```bash
roslaunch openni_launch openni.launch
```

Inicia o driver do controlador, substitua <endereco_ip_robo> pelo endereço ip do controlador, caso esteja mexendo com o manipulador, ou pelo endereço ip do computador, caso seja uma simulação no RT Toolbox 3.

```bash
roslaunch melfa_driver melfa_driver.launch robot_ip:=<endereco_ip_robo>
```

Inicie o programa deste repositório

```bash
roslaunch img2joint img2joint.launch
```

A cor do objeto a ser rastreado deve ser mudada no código disponível em `catkin_ws/src/img2joint/script/img2jointController.python` nas linhas 39 e 40 que controlam o limite inferior e superior da cor que deseja-se rastrear, estas devem ser descritas no espaço de cores HSV (sugestão: utilize o gimp para determinar o valor da cor e utilize apenas o valor de H com uma variação de 10 unidades a mais e a menos para os limites). 

## Video Demo do Funcionamento 🎥
