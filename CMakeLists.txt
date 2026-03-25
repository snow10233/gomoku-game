# 1. 指定 CMake 最低版本要求 (通常 VS Code/WSL 內建的都比這高)
cmake_minimum_required(VERSION 3.10)

# 2. 設定專案名稱與使用的語言 (CXX 代表 C++)
project(GomokuGame CXX)

# 3. 告訴編譯器去哪裡找標頭檔 (.h)
# ${PROJECT_SOURCE_DIR} 代表你專案的根目錄
include_directories(${PROJECT_SOURCE_DIR}/include)

# 4. 把 src 資料夾底下的 .cpp 檔案整理起來
set(SOURCES
    src/main.cpp
    src/board.cpp
    src/position.cpp
)
# 告訴 CMake 匯出編譯指令的詳細資訊
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# 5. 將這些原始碼編譯成執行檔，名稱設定為 gomoku
add_executable(gomoku ${SOURCES})