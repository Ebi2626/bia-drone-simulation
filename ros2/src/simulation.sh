#!/bin/bash

# 1. Ustalenie ścieżki bazowej
BASE_DIR=$(pwd)
SRC_DIR="$BASE_DIR"

# 2. Wskazanie nazwy świata (argument skryptu, np. ./run.sh simple)
WORLD_NAME=${1:-simple}
WORLD_FILE="$SRC_DIR/worlds/$WORLD_NAME.world"
PX4_WORK_DIR="$HOME/PX4-Autopilot"

# Sprawdzenie czy plik świata istnieje
if [ ! -f "$WORLD_FILE" ]; then
    echo "Błąd: Nie znaleziono pliku świata: $WORLD_FILE"
    exit 1
fi

# ---------------------------------------------------------
# KONFIGURACJA DLA GAZEBO CLASSIC (Gazebo 11)
# ---------------------------------------------------------

# 3. Ścieżki do modeli (Twoje huge_building)
# Gazebo Classic używa GAZEBO_MODEL_PATH
export GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:$SRC_DIR/models

# 4. Ścieżki do zasobów (aby Gazebo widziało tekstury/światy)
# Gazebo Classic używa GAZEBO_RESOURCE_PATH
export GAZEBO_RESOURCE_PATH=$GAZEBO_RESOURCE_PATH:$SRC_DIR/worlds

# 5. Informacja dla PX4, jaki świat załadować
# W Classic używamy zmiennej PX4_SITL_WORLD wskazującej na PEŁNĄ ścieżkę
export PX4_SITL_WORLD=$WORLD_FILE

export PX4_GZ_MODEL_POSE="2662.302490,-2583.753174,-54.242710,0,0,-2.335825"

echo ">>> Konfiguracja dla Gazebo Classic"
echo ">>> Świat: $PX4_SITL_WORLD"
echo ">>> Modele: $SRC_DIR/models"

# Auto-naprawa symlinku, jeśli go brakuje
if [ ! -L "$HOME/PX4-Autopilot" ]; then
    echo ">>> Tworzenie brakującego symlinku do PX4..."
    ln -s /opt/PX4-Autopilot $HOME/PX4-Autopilot
fi

# 6. Uruchomienie PX4 SITLQ
# WAŻNE: Target to 'gazebo', a nie 'gz_x500'
# Domyślny model drona dla Classic to zazwyczaj 'iris' lub 'x500'
cd ~/PX4-Autopilot

if [ -d "$PX4_WORK_DIR" ]; then
    # Sprawdź, czy folder należy do mnie. Jeśli nie - przejmij go.
    if [ ! -O "$PX4_WORK_DIR" ]; then
        echo ">>> Wykryto błędne uprawnienia (root?). Naprawianie..."
        # Zakładam, że masz sudo bez hasła (standard w kontenerach deweloperskich)
        sudo chown -R $(whoami) "$PX4_WORK_DIR"
    fi
fi

# Jeśli używasz PX4 v1.14+, target to zazwyczaj 'px4_sitl gazebo-classic' lub po prostu 'gazebo'
# Najbezpieczniejsza komenda dla Classic:
make px4_sitl gazebo
