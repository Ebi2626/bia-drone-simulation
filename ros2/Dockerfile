# Dockerfile dla ROS2 Jazzy z obsługą GUI
FROM ros:jazzy

# Ustawienie argumentów dla nieinteraktywnej instalacji
ARG DEBIAN_FRONTEND=noninteractive

# Zachowanie zmiennej środowiskowej DISPLAY
ENV DISPLAY=:0

# Aktualizacja systemu i instalacja podstawowych zależności
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y \
    # Narzędzia podstawowe
    build-essential \
    ca-certificates \
    curl \
    wget \
    git \
    vim \
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
    # Nowoczesne pakiety OpenGL Mesa (zastąpienie libgl1-mesa-glx)
    libgl1 \
    libglx-mesa0 \
    libgl1-mesa-dri \
    mesa-utils \
    x11-apps \
    # Pakiety ROS2 desktop z narzędziami GUI
    ros-jazzy-desktop \
    ros-jazzy-rviz2 \
    # Narzędzia deweloperskie Python
    python3-pip \
    python3-colcon-common-extensions \
    python3-rosdep \
    && rm -rf /var/lib/apt/lists/*

# Inicjalizacja rosdep
RUN rosdep update

# Ustawienie katalogu roboczego
WORKDIR /ros2_ws

# Automatyczne ładowanie środowiska ROS2 przy starcie bash
RUN echo "source /opt/ros/jazzy/setup.bash" >> /root/.bashrc && \
    echo "echo 'ROS2 Jazzy environment loaded'" >> /root/.bashrc

# Ustawienie QT_X11_NO_MITSHM dla lepszej kompatybilności z X11
ENV QT_X11_NO_MITSHM=1

# Domyślny punkt wejścia
CMD ["/bin/bash"]
