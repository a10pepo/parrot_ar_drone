FROM ubuntu:16.04
#**************************************** INSTALLLING java ******************************
RUN apt-get -y update
RUN apt-get -y upgrade 
RUN apt-get -y install openjdk-8-jdk
ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64
ENV PATH $PATH:/usr/lib/jvm/java-8-openjdk-amd64/bin
RUN echo "export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64" >>~/.bash_profile
RUN echo "export PATH=$PATH:/usr/lib/jvm/java-8-openjdk-amd64/bin" >>~/.bash_profile

#**************************************** INSTALLING Olympe Parrot ******************************

RUN apt-get -y update
RUN apt-get -y upgrade 
RUN echo "##################################"
RUN echo "## INSTALLATION OLYMPE PARROT  ##"
RUN echo "##################################"
RUN apt -y install repo
RUN mkdir -p code/parrot-groundsdk
RUN cd code/parrot-groundsdk 
RUN repo init -u https://github.com/Parrot-Developers/groundsdk-manifest.git
RUN repo sync
RUN ./products/olympe/linux/env/postinst
RUN ./build.sh -p olympe-linux -A all final -j

#**************************************** INSTALLING Olympe Parrot ******************************
RUN useradd -m  -s /bin/bash parrot
RUN apt-get -y update
RUN apt-get -y upgrade 
RUN echo "##################################"
RUN echo "## INSTALLATION SPHINX PARROT  ##"
RUN echo "##################################"
RUN apt -y install mesa-utils
RUN echo "deb http://plf.parrot.com/sphinx/binary `lsb_release -cs`/" | sudo tee /etc/apt/sources.list.d/sphinx.list > /dev/null
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 508B1AE5
RUN apt-get -y install parrot-sphinx
RUN systemctl start firmwared.service
RUN usermod -aG firmwared parrot

