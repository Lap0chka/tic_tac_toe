# 🕹️ Tic Tac Toe in Python

## 📌 Project Description

**Tic Tac Toe** is a console-based implementation of the classic game, designed using Python. This project serves as an example of object-oriented programming (OOP) principles, showcasing concepts like **inheritance**, **encapsulation**, **polymorphism**, **abstraction**, and the **Singleton pattern**.

The game includes two modes:
1. **Player vs. Player** - Two users play against each other.
2. **Player vs. Computer** - A user competes against an AI.

The project also incorporates modern Python tools for code quality and maintainability:
- **Black** for automatic code formatting.
- **Flake8** for linting and static code analysis.
- **Mypy** for type checking.
- **isort** for organizing imports.
- **unittest** for testing.

## 🛠️ OOP Principles Used

### 1. **Encapsulation**
   - Game state and player actions are encapsulated within classes, preventing direct modification of critical data.

### 2. **Inheritance**
   - The `Player` class serves as a base class, allowing the creation of specific player types like `HumanPlayer` and `AIPlayer`.

### 3. **Polymorphism**
   - Common methods like `make_move()` are overridden in subclasses, enabling diverse behavior while maintaining a unified interface.

### 4. **Abstraction**
   - Abstract methods define the essential behaviors for players, ensuring consistent functionality across different implementations.

### 5. **Singleton Pattern**
   - The game board is implemented using the Singleton pattern to ensure a single shared state of the board throughout the game. This pattern prevents the creation of multiple board instances, maintaining consistency in the game's state.

### Why Singleton for the Tic Tac Toe Board?
   - In Tic Tac Toe, having a single shared board across players is critical. The Singleton pattern guarantees that all actions modify the same board instance, avoiding conflicts or synchronization issues during gameplay.

## 📂 Project Structure

```plaintext
tic_tac_toe/
│   tictactoe
│    ├── logger.py          # logginh
├    ├── test.py            # test
│    ├── board.py           # main logic
├── main.py          # Entry point of the application
│
├── requirements.txt # Project dependencies
└── README.md        # Project documentation
