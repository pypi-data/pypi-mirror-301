#include <iostream>
#include <vector>
#include <conio.h>
#include <windows.h>
#include <ctime>

using namespace std;

const int width = 20;
const int height = 20;

class Snake {
private:
    vector<pair<int, int>> body;
    int direction;
    pair<int, int> food;

public:
    Snake() {
        body.push_back({width / 2, height / 2});
        direction = 0;
        generateFood();
    }

    void generateFood() {
        srand(time(0));
        food = {rand() % width, rand() % height};
    }

    void move() {
        pair<int, int> newHead = body.front();
        switch (direction) {
            case 0: newHead.second--; break; // Up
            case 1: newHead.first++; break;  // Right
            case 2: newHead.second++; break; // Down
            case 3: newHead.first--; break;  // Left
        }

        if (newHead == food) {
            body.insert(body.begin(), newHead);
            generateFood();
        } else {
            body.insert(body.begin(), newHead);
            body.pop_back();
        }
    }

    bool isGameOver() {
        pair<int, int> head = body.front();
        if (head.first < 0 || head.first >= width || head.second < 0 || head.second >= height)
            return true;

        for (int i = 1; i < body.size(); i++)
            if (body[i] == head)
                return true;

        return false;
    }

    void changeDirection(char key) {
        switch (key) {
            case 'w': if (direction != 2) direction = 0; break;
            case 'd': if (direction != 3) direction = 1; break;
            case 's': if (direction != 0) direction = 2; break;
            case 'a': if (direction != 1) direction = 3; break;
        }
    }

    void draw() {
        system("cls");
        vector<vector<char>> board(height, vector<char>(width, ' '));

        for (auto& segment : body)
            board[segment.second][segment.first] = 'O';

        board[food.second][food.first] = 'F';

        for (int i = 0; i < height; i++) {
            for (int j = 0; j < width; j++)
                cout << board[i][j] << ' ';
            cout << endl;
        }
    }
};

int main() {
    Snake snake;
    char key;

    while (!snake.isGameOver()) {
        snake.draw();
        if (_kbhit()) {
            key = _getch();
            snake.changeDirection(key);
        }
        snake.move();
        Sleep(100);
    }

    cout << "Game Over!" << endl;
    return 0;
}
