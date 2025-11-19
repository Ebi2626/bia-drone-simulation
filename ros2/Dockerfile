# Dockerfile dla ROS2 Jazzy z PX4 SITL i Gazebo dla symulacji roju dronów
FROM ros:jazzy

# Ustaw bash jako domyślną shell dla RUN commands
SHELL ["/bin/bash", "-c"]

# Ustawienia dla nieinteraktywnej instalacji
ARG DEBIAN_FRONTEND=noninteractive

# Zmienne środowiskowe
ENV DISPLAY=:0
ENV QT_X11_NO_MITSHM=1
ENV PX4_HOME_LAT=47.397742
ENV PX4_HOME_LON=8.545594
ENV PX4_HOME_ALT=488.0

# ============================================
# SEKCJA 1: Podstawowe narzędzia i zależności
# ============================================
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y \
    # Narzędzia podstawowe
    build-essential \
    ca-certificates \
    curl \
    wget \
    git \
    vim \
    nano \
    sudo \
    lsb-release \
    gnupg2 \
    # Biblioteki X11 i Qt dla GUI
    libxcb-icccm4 \
    libxcb-image0 \
    libxcb-keysyms1 \
    libxcb-randr0 \
    libxcb-render-util0 \
    libxcb-xfixes0 \
    libxcb-xinerama0 \
    libxkbcommon-x11-0 \
    libxcb-cursor0 \
    # OpenGL Mesa
    libgl1 \
    libglx-mesa0 \
    libgl1-mesa-dri \
    mesa-utils \
    x11-apps \
    # Pakiety ROS2 desktop
    ros-jazzy-desktop \
    ros-jazzy-rviz2 \
    # Narzędzia deweloperskie Python
    python3-pip \
    python3-colcon-common-extensions \
    python3-rosdep \
    python3-vcstool \
    python3-setuptools \
    python3-empy \
    python3-toml \
    python3-numpy \
    python3-yaml \
    python3-dev \
    # Dodatkowe narzędzia do kompilacji
    cmake \
    ninja-build \
    ccache \
    && rm -rf /var/lib/apt/lists/*

# ============================================
# SEKCJA 2: Instalacja Gazebo Harmonic
# ============================================
RUN wget https://packages.osrfoundation.org/gazebo.gpg -O /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] http://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" | \
    tee /etc/apt/sources.list.d/gazebo-stable.list > /dev/null && \
    apt-get update && \
    apt-get install -y \
    gz-harmonic \
    ros-jazzy-ros-gz \
    libgz-sim8-dev \
    libgstreamer1.0-dev \
    libgstreamer-plugins-base1.0-dev \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-bad \
    gstreamer1.0-libav \
    && rm -rf /var/lib/apt/lists/*

# ============================================
# SEKCJA 3: Instalacja PX4 Autopilot (jako root w /opt)
# ============================================

WORKDIR /opt
RUN git clone https://github.com/PX4/PX4-Autopilot.git --recursive && \
    cd PX4-Autopilot && \
    bash ./Tools/setup/ubuntu.sh --no-nuttx --no-sim-tools && \
    pip3 install --break-system-packages -r Tools/setup/requirements.txt

# Instalacja zależności PX4
RUN cd /opt/PX4-Autopilot && \
    bash ./Tools/setup/ubuntu.sh --no-nuttx --no-sim-tools && \
    pip3 install --break-system-packages -r Tools/setup/requirements.txt

# ============================================
# SEKCJA 4: Instalacja Micro XRCE-DDS Agent
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
# SEKCJA 5: Workspace ROS2 z px4_msgs
# ============================================
RUN mkdir -p /opt/ros2_ws/src && \
    cd /opt/ros2_ws/src && \
    git clone https://github.com/PX4/px4_msgs.git && \
    git clone https://github.com/PX4/px4_ros_com.git

# Kompilacja workspace ROS2
RUN /bin/bash -c "source /opt/ros/jazzy/setup.bash && \
    cd /opt/ros2_ws && \
    colcon build --symlink-install"

# ============================================
# SEKCJA 7: Konfiguracja użytkownika
# ============================================
# Sprawdź czy użytkownik z UID 1000 istnieje, jeśli nie - utwórz
RUN if id -u 1000 > /dev/null 2>&1; then \
        USERNAME=$(id -un 1000); \
        echo "Using existing user: $USERNAME (UID 1000)"; \
    else \
        groupadd --gid 1000 ros2user && \
        useradd --uid 1000 --gid 1000 -m ros2user -s /bin/bash && \
        USERNAME=ros2user; \
        echo "Created new user: $USERNAME (UID 1000)"; \
    fi && \
    echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/$USERNAME && \
    chmod 0440 /etc/sudoers.d/$USERNAME

# Utwórz symlinki w katalogu domowym użytkownika (oszczędza miejsce)
RUN USERNAME=$(id -un 1000 2>/dev/null || echo "ubuntu") && \
    su - $USERNAME -c "ln -s /opt/PX4-Autopilot ~/PX4-Autopilot" && \
    su - $USERNAME -c "ln -s /opt/ros2_ws ~/ros2_ws" && \
    su - $USERNAME -c "mkdir -p ~/scripts"

# ============================================
# SEKCJA 8: Konfiguracja środowiska (.bashrc)
# ============================================
RUN USERNAME=$(id -un 1000 2>/dev/null || echo "ubuntu") && \
    echo "" >> /home/$USERNAME/.bashrc && \
    echo "# ==========================================" >> /home/$USERNAME/.bashrc && \
    echo "# ROS2 Jazzy + PX4 SITL Environment" >> /home/$USERNAME/.bashrc && \
    echo "# ==========================================" >> /home/$USERNAME/.bashrc && \
    echo "" >> /home/$USERNAME/.bashrc && \
    echo "# ROS2 Jazzy" >> /home/$USERNAME/.bashrc && \
    echo "source /opt/ros/jazzy/setup.bash" >> /home/$USERNAME/.bashrc && \
    echo "source /opt/ros2_ws/install/setup.bash" >> /home/$USERNAME/.bashrc && \
    echo "" >> /home/$USERNAME/.bashrc && \
    echo "# PX4 Environment" >> /home/$USERNAME/.bashrc && \
    echo "export PX4_DIR=~/PX4-Autopilot" >> /home/$USERNAME/.bashrc && \
    echo "export PATH=\$PATH:\$HOME/.local/bin" >> /home/$USERNAME/.bashrc && \
    echo "" >> /home/$USERNAME/.bashrc && \
    echo "# Gazebo Environment for PX4" >> /home/$USERNAME/.bashrc && \
    echo "export GZ_SIM_RESOURCE_PATH=\$GZ_SIM_RESOURCE_PATH:~/PX4-Autopilot/Tools/simulation/gz/models" >> /home/$USERNAME/.bashrc && \
    echo "export GZ_SIM_SYSTEM_PLUGIN_PATH=\$GZ_SIM_SYSTEM_PLUGIN_PATH:~/PX4-Autopilot/build/px4_sitl_default/build_gz-harmonic" >> /home/$USERNAME/.bashrc && \
    echo "" >> /home/$USERNAME/.bashrc && \
    echo "# Useful Aliases" >> /home/$USERNAME/.bashrc && \
    echo "alias px4_build='cd ~/PX4-Autopilot && make px4_sitl gz_x500'" >> /home/$USERNAME/.bashrc && \
    echo "alias px4_clean='cd ~/PX4-Autopilot && make clean && make distclean'" >> /home/$USERNAME/.bashrc && \
    echo "alias start_agent='MicroXRCEAgent udp4 -p 8888'" >> /home/$USERNAME/.bashrc && \
    echo "alias ros2_topics='ros2 topic list'" >> /home/$USERNAME/.bashrc && \
    echo "" >> /home/$USERNAME/.bashrc && \
    echo "# Welcome Message" >> /home/$USERNAME/.bashrc && \
    echo "echo '==========================================='" >> /home/$USERNAME/.bashrc && \
    echo "echo '   ROS2 Jazzy + PX4 SITL Environment'" >> /home/$USERNAME/.bashrc && \
    echo "echo '==========================================='" >> /home/$USERNAME/.bashrc && \
    echo "echo 'Quick start commands:'" >> /home/$USERNAME/.bashrc && \
    echo "echo '  px4_build       - Build and run PX4 SITL'" >> /home/$USERNAME/.bashrc && \
    echo "echo '  start_agent     - Start Micro XRCE-DDS Agent'" >> /home/$USERNAME/.bashrc && \
    echo "echo '  ros2_topics     - List ROS2 topics'" >> /home/$USERNAME/.bashrc && \
    echo "echo '==========================================='" >> /home/$USERNAME/.bashrc && \
    echo "" >> /home/$USERNAME/.bashrc

# ============================================
# SEKCJA 9: Skrypty pomocnicze
# ============================================
# Skrypt do budowania pojedynczego drona
RUN USERNAME=$(id -un 1000 2>/dev/null || echo "ubuntu") && \
    echo '#!/bin/bash' > /home/$USERNAME/scripts/build_px4.sh && \
    echo 'cd ~/PX4-Autopilot' >> /home/$USERNAME/scripts/build_px4.sh && \
    echo 'make px4_sitl gz_x500' >> /home/$USERNAME/scripts/build_px4.sh && \
    chmod +x /home/$USERNAME/scripts/build_px4.sh

# Skrypt do uruchamiania roju dronów
RUN USERNAME=$(id -un 1000 2>/dev/null || echo "ubuntu") && \
    echo '#!/bin/bash' > /home/$USERNAME/scripts/start_swarm.sh && \
    echo '# Start multiple PX4 instances for swarm simulation' >> /home/$USERNAME/scripts/start_swarm.sh && \
    echo 'NUM_DRONES=${1:-3}' >> /home/$USERNAME/scripts/start_swarm.sh && \
    echo 'echo "Starting $NUM_DRONES drones..."' >> /home/$USERNAME/scripts/start_swarm.sh && \
    echo 'cd ~/PX4-Autopilot' >> /home/$USERNAME/scripts/start_swarm.sh && \
    echo '' >> /home/$USERNAME/scripts/start_swarm.sh && \
    echo 'for i in $(seq 0 $(($NUM_DRONES-1))); do' >> /home/$USERNAME/scripts/start_swarm.sh && \
    echo '    PX4_SYS_AUTOSTART=4001 \' >> /home/$USERNAME/scripts/start_swarm.sh && \
    echo '    PX4_SIM_MODEL=gz_x500 \' >> /home/$USERNAME/scripts/start_swarm.sh && \
    echo '    PX4_GZ_MODEL_POSE="$((i*3)),0,0,0,0,0" \' >> /home/$USERNAME/scripts/start_swarm.sh && \
    echo '    ./build/px4_sitl_default/bin/px4 -i $i &' >> /home/$USERNAME/scripts/start_swarm.sh && \
    echo '    echo "Started drone $i"' >> /home/$USERNAME/scripts/start_swarm.sh && \
    echo '    sleep 2' >> /home/$USERNAME/scripts/start_swarm.sh && \
    echo 'done' >> /home/$USERNAME/scripts/start_swarm.sh && \
    echo '' >> /home/$USERNAME/scripts/start_swarm.sh && \
    echo 'echo "All drones started. Press Ctrl+C to stop."' >> /home/$USERNAME/scripts/start_swarm.sh && \
    echo 'wait' >> /home/$USERNAME/scripts/start_swarm.sh && \
    chmod +x /home/$USERNAME/scripts/start_swarm.sh

# Skrypt do pełnej symulacji z agentem
RUN USERNAME=$(id -un 1000 2>/dev/null || echo "ubuntu") && \
    echo '#!/bin/bash' > /home/$USERNAME/scripts/start_simulation.sh && \
    echo 'echo "Starting PX4 SITL with Micro XRCE-DDS Agent..."' >> /home/$USERNAME/scripts/start_simulation.sh && \
    echo 'echo "Agent will start in background, PX4 in foreground"' >> /home/$USERNAME/scripts/start_simulation.sh && \
    echo '' >> /home/$USERNAME/scripts/start_simulation.sh && \
    echo '# Start Agent in background' >> /home/$USERNAME/scripts/start_simulation.sh && \
    echo 'MicroXRCEAgent udp4 -p 8888 &' >> /home/$USERNAME/scripts/start_simulation.sh && \
    echo 'AGENT_PID=$!' >> /home/$USERNAME/scripts/start_
