# Dockerfile dla ROS2 Humble (Ubuntu 22.04) z PX4 v1.14 i Gazebo Classic
# To jest JEDYNA stabilna kombinacja dla Twoich badań.
FROM ros:humble

SHELL ["/bin/bash", "-c"]
ARG DEBIAN_FRONTEND=noninteractive

# Zmienne środowiskowe
ENV DISPLAY=:0
ENV QT_X11_NO_MITSHM=1

# ============================================
# SEKCJA 1: Podstawowe narzędzia i zależności
# ============================================
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y \
    build-essential git wget curl vim nano sudo lsb-release gnupg2 \
    libxcb-xinerama0 libxkbcommon-x11-0 libxcb-cursor0 \
    mesa-utils x11-apps \
    # DODANE ZALEŻNOŚCI DLA GAZEBO CLASSIC:
    libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev \
    gstreamer1.0-plugins-base gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly \
    # Pakiety ROS2 Humble
    ros-humble-desktop \
    ros-humble-rviz2 \
    # Python
    python3-pip python3-colcon-common-extensions python3-rosdep \
    python3-vcstool python3-numpy python3-dev python3-setuptools \
    # Build tools
    cmake ninja-build ccache \
    && rm -rf /var/lib/apt/lists/*

# ============================================
# SEKCJA 2: Instalacja Gazebo Classic
# ============================================
# Najpierw upewniamy się, że mamy dostęp do wszystkich repozytoriów Ubuntu
RUN apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository universe && \
    add-apt-repository multiverse && \
    add-apt-repository restricted && \
    apt-get update

# Instalacja Gazebo i pluginów ROS z oficjalnych repozytoriów Ubuntu/ROS
RUN apt-get install -y \
    gazebo \
    libgazebo-dev \
    ros-humble-gazebo-ros-pkgs \
    ros-humble-gazebo-ros2-control \
    && rm -rf /var/lib/apt/lists/*


# ============================================
# SEKCJA 3: Instalacja PX4 Autopilot (v1.14)
# ============================================
WORKDIR /opt
RUN git clone --recursive --branch v1.14.3 https://github.com/PX4/PX4-Autopilot.git && \
    cd PX4-Autopilot && \
    bash ./Tools/setup/ubuntu.sh --no-nuttx --no-sim-tools && \
    pip3 install --no-cache-dir \
        numpy \
        toml \
        pyyaml \
        jinja2 \
        packaging \
        kconfiglib \
        jsonschema \
        future \
        lxml \
        cerberus \
        empy==3.3.4 \
        catkin_pkg

# ============================================
# SEKCJA 4: Micro XRCE-DDS Agent (Poprawiona wersja)
# ============================================
RUN cd /opt && \
    git clone -b v2.4.3 https://github.com/eProsima/Micro-XRCE-DDS-Agent.git && \
    cd Micro-XRCE-DDS-Agent && \
    mkdir build && cd build && \
    cmake .. && \
    make -j$(nproc) && \
    make install && \
    ldconfig /usr/local/lib/

# ============================================
# SEKCJA 5: Workspace ROS2
# ============================================
RUN mkdir -p /opt/ros2_ws/src && \
    cd /opt/ros2_ws/src && \
    git clone https://github.com/PX4/px4_msgs.git && \
    git clone https://github.com/PX4/px4_ros_com.git

RUN /bin/bash -c "source /opt/ros/humble/setup.bash && \
    cd /opt/ros2_ws && \
    colcon build --symlink-install"

# ============================================
# SEKCJA 6: Kompilacja PX4
# ============================================
RUN pip3 install --upgrade kconfiglib jsonschema jinja2 packaging pyyaml numpy

# Kompilacja właściwa
RUN /bin/bash -c "cd /opt/PX4-Autopilot && \
    make distclean && \
    DONT_RUN=1 make px4_sitl gazebo-classic"

# ============================================
# SEKCJA 7: Konfiguracja użytkownika
# ============================================
RUN if id -u 1000 > /dev/null 2>&1; then \
        USERNAME=$(id -un 1000); \
        echo "Using existing user: $USERNAME"; \
    else \
        groupadd --gid 1000 ros2user && \
        useradd --uid 1000 --gid 1000 -m ros2user -s /bin/bash && \
        USERNAME=ros2user; \
        echo "Created new user: $USERNAME"; \
    fi && \
    echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/$USERNAME && \
    chmod 0440 /etc/sudoers.d/$USERNAME && \
    chown -R 1000:1000 /opt/PX4-Autopilot && \
    chown -R 1000:1000 /opt/ros2_ws && \
    chown -R 1000:1000 /opt/Micro-XRCE-DDS-Agent

# ============================================
# SEKCJA 8: Konfiguracja środowiska (.bashrc) (ZMIANA)
# ============================================
RUN USERNAME=$(id -un 1000 2>/dev/null || echo "ubuntu") && \
    echo "" >> /home/$USERNAME/.bashrc && \
    echo "# ==========================================" >> /home/$USERNAME/.bashrc && \
    echo "# ROS2 Humble + PX4 SITL (Gazebo Classic)" >> /home/$USERNAME/.bashrc && \
    echo "# ==========================================" >> /home/$USERNAME/.bashrc && \
    echo "" >> /home/$USERNAME/.bashrc && \
    echo "source /opt/ros/humble/setup.bash" >> /home/$USERNAME/.bashrc && \
    echo "source /opt/ros2_ws/install/setup.bash" >> /home/$USERNAME/.bashrc && \
    echo "source /usr/share/gazebo/setup.sh" >> /home/$USERNAME/.bashrc && \
    echo "" >> /home/$USERNAME/.bashrc && \
    echo "export PX4_DIR=~/PX4-Autopilot" >> /home/$USERNAME/.bashrc && \
    echo "export PATH=\$PATH:\$HOME/.local/bin" >> /home/$USERNAME/.bashrc && \
    echo "" >> /home/$USERNAME/.bashrc && \
    echo "# Gazebo Classic Environment Variables" >> /home/$USERNAME/.bashrc && \
    echo "export GAZEBO_PLUGIN_PATH=\$GAZEBO_PLUGIN_PATH:~/PX4-Autopilot/build/px4_sitl_default/build_gazebo-classic" >> /home/$USERNAME/.bashrc && \
    echo "export GAZEBO_MODEL_PATH=\$GAZEBO_MODEL_PATH:~/PX4-Autopilot/Tools/simulation/gazebo-classic/models" >> /home/$USERNAME/.bashrc && \
    echo "" >> /home/$USERNAME/.bashrc && \
    echo "# Aliases" >> /home/$USERNAME/.bashrc && \
    echo "alias px4_build='cd ~/PX4-Autopilot && make px4_sitl gazebo-classic'" >> /home/$USERNAME/.bashrc && \
    echo "alias px4_clean='cd ~/PX4-Autopilot && make clean && make distclean'" >> /home/$USERNAME/.bashrc && \
    echo "alias start_agent='MicroXRCEAgent udp4 -p 8888'" >> /home/$USERNAME/.bashrc && \
    echo "" >> /home/$USERNAME/.bashrc

# ============================================
# SEKCJA 9: Skrypty pomocnicze (ZMIANA)
# ============================================
# ============================================
# SEKCJA 9: Skrypty pomocnicze (POPRAWIONA)
# ============================================

# Skrypt do budowania pojedynczego drona (Classic)
# ZMIANA: Dodano jawne mkdir -p przed zapisem pliku
RUN USERNAME=$(id -un 1000 2>/dev/null || echo "ubuntu") && \
    mkdir -p /home/$USERNAME/scripts && \
    echo '#!/bin/bash' > /home/$USERNAME/scripts/build_px4.sh && \
    echo 'cd ~/PX4-Autopilot' >> /home/$USERNAME/scripts/build_px4.sh && \
    echo 'make px4_sitl gazebo-classic' >> /home/$USERNAME/scripts/build_px4.sh && \
    chmod +x /home/$USERNAME/scripts/build_px4.sh && \
    chown -R $USERNAME:$USERNAME /home/$USERNAME/scripts


# Skrypt do uruchamiania roju dronów (Dostosowany do Classic)
RUN USERNAME=$(id -un 1000 2>/dev/null || echo "ubuntu") && \
    mkdir -p /home/$USERNAME/scripts && \
    echo '#!/bin/bash' > /home/$USERNAME/scripts/start_swarm.sh && \
    echo '# Start multiple PX4 instances for swarm simulation in Gazebo Classic' >> /home/$USERNAME/scripts/start_swarm.sh && \
    echo 'NUM_DRONES=${1:-3}' >> /home/$USERNAME/scripts/start_swarm.sh && \
    echo 'cd ~/PX4-Autopilot' >> /home/$USERNAME/scripts/start_swarm.sh && \
    echo '' >> /home/$USERNAME/scripts/start_swarm.sh && \
    echo '# Kill existing simulation' >> /home/$USERNAME/scripts/start_swarm.sh && \
    echo 'pkill -x px4 || true' >> /home/$USERNAME/scripts/start_swarm.sh && \
    echo 'pkill -x gazebo || true' >> /home/$USERNAME/scripts/start_swarm.sh && \
    echo 'pkill -x gzserver || true' >> /home/$USERNAME/scripts/start_swarm.sh && \
    echo 'pkill -x gzclient || true' >> /home/$USERNAME/scripts/start_swarm.sh && \
    echo 'sleep 2' >> /home/$USERNAME/scripts/start_swarm.sh && \
    echo '' >> /home/$USERNAME/scripts/start_swarm.sh && \
    echo '# Note: For robust swarm in Classic, we usually use Tools/simulation/gazebo-classic/sitl_multiple_run.sh' >> /home/$USERNAME/scripts/start_swarm.sh && \
    echo '# But here is a manual loop approach compatible with the docker setup:' >> /home/$USERNAME/scripts/start_swarm.sh && \
    echo 'for ((i=0; i<NUM_DRONES; i++)); do' >> /home/$USERNAME/scripts/start_swarm.sh && \
    echo '    echo "Starting drone $i..."' >> /home/$USERNAME/scripts/start_swarm.sh && \
    echo '    # Classic uses px4_sitl with instance ID' >> /home/$USERNAME/scripts/start_swarm.sh && \
    echo '    PX4_SYS_AUTOSTART=4001 \' >> /home/$USERNAME/scripts/start_swarm.sh && \
    echo '    PX4_SIM_MODEL=iris \' >> /home/$USERNAME/scripts/start_swarm.sh && \
    echo '    PX4_GZ_MODEL_POSE="$((i*2)),0,0,0,0,0" \' >> /home/$USERNAME/scripts/start_swarm.sh && \
    echo '    ./build/px4_sitl_default/bin/px4 -i $i &' >> /home/$USERNAME/scripts/start_swarm.sh && \
    echo '    sleep 4' >> /home/$USERNAME/scripts/start_swarm.sh && \
    echo 'done' >> /home/$USERNAME/scripts/start_swarm.sh && \
    echo '' >> /home/$USERNAME/scripts/start_swarm.sh && \
    echo 'echo "Swarm started. Launch Gazebo GUI manually if needed: gazebo --verbose"' >> /home/$USERNAME/scripts/start_swarm.sh && \
    chmod +x /home/$USERNAME/scripts/start_swarm.sh && \
    chown -R $USERNAME:$USERNAME /home/$USERNAME/scripts
    
USER $USERNAME
WORKDIR /home/$USERNAME
CMD ["/bin/bash"]
