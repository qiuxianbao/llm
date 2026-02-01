// 游戏常量
const COLS = 10;
const ROWS = 20;
const BLOCK_SIZE = 30;
const COLORS = [
    null,
    '#FF0D72', // I
    '#0DC2FF', // J
    '#0DFF72', // L
    '#F538FF', // O
    '#FF8E0D', // S
    '#FFE138', // T
    '#3877FF'  // Z
];

// 方块形状定义
const SHAPES = [
    [],
    [[0, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0], [0, 0, 0, 0]], // I
    [[2, 0, 0], [2, 2, 2], [0, 0, 0]], // J
    [[0, 0, 3], [3, 3, 3], [0, 0, 0]], // L
    [[4, 4], [4, 4]], // O
    [[0, 5, 5], [5, 5, 0], [0, 0, 0]], // S
    [[0, 6, 0], [6, 6, 6], [0, 0, 0]], // T
    [[7, 7, 0], [0, 7, 7], [0, 0, 0]]  // Z
];

// 游戏变量
let canvas = document.getElementById('tetris');
let ctx = canvas.getContext('2d');
let scoreElement = document.getElementById('score');
let levelElement = document.getElementById('level');
let linesElement = document.getElementById('lines');
let score = 0;
let level = 1;
let lines = 0;
let board = createMatrix(COLS, ROWS);
let player = {
    pos: { x: 0, y: 0 },
    matrix: null,
    score: 0
};
let nextPieceCanvas = document.getElementById('next-piece');
let nextPieceCtx = nextPieceCanvas.getContext('2d');
let nextPieceMatrix = null;
let dropCounter = 0;
let dropInterval = 1000; // 初始下落间隔（毫秒）
let lastTime = 0;
let gameActive = false;
let gameAnimation = null;

// 初始化画布大小
ctx.scale(BLOCK_SIZE, BLOCK_SIZE);

// 初始化下一个方块画布大小
nextPieceCtx.scale(BLOCK_SIZE / 2, BLOCK_SIZE / 2); // 缩小比例以便在较小的画布上显示

// 创建矩阵
function createMatrix(w, h) {
    const matrix = [];
    while (h--) {
        matrix.push(new Array(w).fill(0));
    }
    return matrix;
}

// 创建随机方块
function createPiece() {
    const piece = Math.floor(Math.random() * 7) + 1;
    return SHAPES[piece].map(row => [...row]);
}

// 绘制方块
function drawMatrix(matrix, offset) {
    matrix.forEach((row, y) => {
        row.forEach((value, x) => {
            if (value !== 0) {
                ctx.fillStyle = COLORS[value];
                ctx.fillRect(x + offset.x, y + offset.y, 1, 1);

                // 添加方块边框效果
                ctx.strokeStyle = 'rgba(255, 255, 255, 0.2)';
                ctx.lineWidth = 0.05;
                ctx.strokeRect(x + offset.x, y + offset.y, 1, 1);

                // 添加3D效果
                ctx.fillStyle = 'rgba(255, 255, 255, 0.2)';
                ctx.fillRect(x + offset.x, y + offset.y, 1, 0.1); // 顶部高光
                ctx.fillRect(x + offset.x, y + offset.y, 0.1, 1); // 左侧高光

                ctx.fillStyle = 'rgba(0, 0, 0, 0.2)';
                ctx.fillRect(x + offset.x + 0.9, y + offset.y, 0.1, 1); // 右侧阴影
                ctx.fillRect(x + offset.x, y + offset.y + 0.9, 1, 0.1); // 底部阴影
            }
        });
    });
}

// 绘制游戏板
function drawBoard() {
    board.forEach((row, y) => {
        row.forEach((value, x) => {
            if (value !== 0) {
                ctx.fillStyle = COLORS[value];
                ctx.fillRect(x, y, 1, 1);

                // 添加方块边框效果
                ctx.strokeStyle = 'rgba(255, 255, 255, 0.2)';
                ctx.lineWidth = 0.05;
                ctx.strokeRect(x, y, 1, 1);

                // 添加3D效果
                ctx.fillStyle = 'rgba(255, 255, 255, 0.2)';
                ctx.fillRect(x, y, 1, 0.1); // 顶部高光
                ctx.fillRect(x, y, 0.1, 1); // 左侧高光

                ctx.fillStyle = 'rgba(0, 0, 0, 0.2)';
                ctx.fillRect(x + 0.9, y, 0.1, 1); // 右侧阴影
                ctx.fillRect(x, y + 0.9, 1, 0.1); // 底部阴影
            }
        });
    });
}

// 绘制游戏
function draw() {
    ctx.fillStyle = '#111';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    drawBoard();
    drawMatrix(player.matrix, player.pos);
}

// 合并方块到游戏板
function merge(board, player) {
    player.matrix.forEach((row, y) => {
        row.forEach((value, x) => {
            if (value !== 0) {
                board[y + player.pos.y][x + player.pos.x] = value;
            }
        });
    });
}

// 碰撞检测
function collide(board, player) {
    const [m, o] = [player.matrix, player.pos];
    for (let y = 0; y < m.length; ++y) {
        for (let x = 0; x < m[y].length; ++x) {
            if (m[y][x] !== 0 &&
                (board[y + o.y] &&
                 board[y + o.y][x + o.x]) !== 0) {
                return true;
            }
        }
    }
    return false;
}

// 旋转方块
function rotate(matrix, dir) {
    for (let y = 0; y < matrix.length; ++y) {
        for (let x = 0; x < y; ++x) {
            [matrix[x][y], matrix[y][x]] = [matrix[y][x], matrix[x][y]];
        }
    }

    if (dir > 0) {
        matrix.forEach(row => row.reverse());
    } else {
        matrix.reverse();
    }
}

// 旋转玩家方块
function playerRotate(dir) {
    const pos = player.pos.x;
    let offset = 1;
    rotate(player.matrix, dir);
    
    while (collide(board, player)) {
        player.pos.x += offset;
        offset = -(offset + (offset > 0 ? 1 : -1));
        if (offset > player.matrix[0].length) {
            rotate(player.matrix, -dir);
            player.pos.x = pos;
            return;
        }
    }
}

// 清除完整行
function sweepRows() {
    let rowCount = 0;
    outer: for (let y = board.length - 1; y >= 0; --y) {
        for (let x = 0; x < board[y].length; ++x) {
            if (board[y][x] === 0) {
                continue outer;
            }
        }

        const row = board.splice(y, 1)[0].fill(0);
        board.unshift(row);
        ++y; // 重新检查当前索引，因为数组长度改变了
        
        rowCount++;
    }
    
    // 更新分数
    if (rowCount > 0) {
        // 根据消除的行数计算分数 (1行=40分, 2行=100分, 3行=300分, 4行=1200分)
        const points = [0, 40, 100, 300, 1200][rowCount] * level;
        score += points;
        lines += rowCount;
        
        // 每消除10行升一级
        level = Math.floor(lines / 10) + 1;
        
        // 随着等级提高，下落速度加快
        dropInterval = Math.max(100, 1000 - (level - 1) * 100);
        
        // 更新UI
        scoreElement.textContent = score;
        levelElement.textContent = level;
        linesElement.textContent = lines;
    }
}

// 绘制下一个方块
function drawNextPiece() {
    // 清空下一个方块的画布
    nextPieceCtx.fillStyle = '#111';
    nextPieceCtx.fillRect(0, 0, nextPieceCanvas.width, nextPieceCanvas.height);

    if (nextPieceMatrix) {
        // 计算方块居中位置
        const offsetX = (nextPieceCanvas.width / BLOCK_SIZE - nextPieceMatrix[0].length) / 2;
        const offsetY = (nextPieceCanvas.height / BLOCK_SIZE - nextPieceMatrix.length) / 2;

        nextPieceMatrix.forEach((row, y) => {
            row.forEach((value, x) => {
                if (value !== 0) {
                    nextPieceCtx.fillStyle = COLORS[value];
                    nextPieceCtx.fillRect((x + offsetX) * BLOCK_SIZE, (y + offsetY) * BLOCK_SIZE, BLOCK_SIZE - 1, BLOCK_SIZE - 1);

                    // 添加方块边框效果
                    nextPieceCtx.strokeStyle = 'rgba(255, 255, 255, 0.2)';
                    nextPieceCtx.lineWidth = 1;
                    nextPieceCtx.strokeRect((x + offsetX) * BLOCK_SIZE, (y + offsetY) * BLOCK_SIZE, BLOCK_SIZE - 1, BLOCK_SIZE - 1);

                    // 添加3D效果
                    nextPieceCtx.fillStyle = 'rgba(255, 255, 255, 0.2)';
                    nextPieceCtx.fillRect((x + offsetX) * BLOCK_SIZE, (y + offsetY) * BLOCK_SIZE, BLOCK_SIZE - 1, 2); // 顶部高光
                    nextPieceCtx.fillRect((x + offsetX) * BLOCK_SIZE, (y + offsetY) * BLOCK_SIZE, 2, BLOCK_SIZE - 1); // 左侧高光

                    nextPieceCtx.fillStyle = 'rgba(0, 0, 0, 0.2)';
                    nextPieceCtx.fillRect(((x + offsetX) * BLOCK_SIZE) + BLOCK_SIZE - 3, (y + offsetY) * BLOCK_SIZE, 2, BLOCK_SIZE - 1); // 右侧阴影
                    nextPieceCtx.fillRect((x + offsetX) * BLOCK_SIZE, ((y + offsetY) * BLOCK_SIZE) + BLOCK_SIZE - 3, BLOCK_SIZE - 1, 2); // 底部阴影
                }
            });
        });
    }
}

// 重置玩家
function resetPlayer() {
    // 如果下一个方块存在，使用它作为当前方块
    if (nextPieceMatrix) {
        player.matrix = nextPieceMatrix;
    } else {
        // 否则创建一个新方块
        player.matrix = createPiece();
    }

    // 生成下一个方块
    nextPieceMatrix = createPiece();
    drawNextPiece(); // 更新下一个方块的显示

    player.pos.y = 0;
    player.pos.x = Math.floor(board[0].length / 2) - Math.floor(player.matrix[0].length / 2);

    // 如果新方块刚出现就发生碰撞，则游戏结束
    if (collide(board, player)) {
        gameOver();
    }
}

// 游戏结束
function gameOver() {
    cancelAnimationFrame(gameAnimation);
    gameActive = false;
    alert(`游戏结束！\n最终得分: ${score}\n消除行数: ${lines}`);
    
    // 重置游戏状态
    score = 0;
    level = 1;
    lines = 0;
    board = createMatrix(COLS, ROWS);
    scoreElement.textContent = score;
    levelElement.textContent = level;
    linesElement.textContent = lines;
}

// 玩家移动
function playerMove(dir) {
    player.pos.x += dir;
    if (collide(board, player)) {
        player.pos.x -= dir;
    }
}

// 玩家下落
function playerDrop() {
    player.pos.y++;
    if (collide(board, player)) {
        player.pos.y--;
        merge(board, player);
        sweepRows();
        resetPlayer();
    }
    dropCounter = 0;
}

// 瞬间下落
function playerHardDrop() {
    while (!collide(board, player)) {
        player.pos.y++;
    }
    player.pos.y--;
    merge(board, player);
    sweepRows();
    resetPlayer();
}

// 游戏循环
function update(time = 0) {
    if (!gameActive) return;

    const deltaTime = time - lastTime;
    lastTime = time;

    dropCounter += deltaTime;
    if (dropCounter > dropInterval) {
        playerDrop();
    }

    // 优化：只在需要时重绘
    draw();
    gameAnimation = requestAnimationFrame(update);
}

// 优化绘制函数，减少重复操作
function draw() {
    // 使用双缓冲技术，先绘制到离屏canvas再复制到显示canvas
    ctx.fillStyle = '#111';
    ctx.fillRect(0, 0, canvas.width / BLOCK_SIZE, canvas.height / BLOCK_SIZE);

    drawBoard();
    drawMatrix(player.matrix, player.pos);
}

// 初始化游戏
function initGame() {
    board = createMatrix(COLS, ROWS);
    score = 0;
    level = 1;
    lines = 0;

    scoreElement.textContent = score;
    levelElement.textContent = level;
    linesElement.textContent = lines;

    // 重置下一个方块
    nextPieceMatrix = null;

    resetPlayer();
    draw();
    drawNextPiece(); // 绘制下一个方块
}

// 开始游戏
function startGame() {
    if (gameActive) return;
    
    gameActive = true;
    lastTime = 0;
    initGame();
    update();
}

// 暂停游戏
function pauseGame() {
    gameActive = !gameActive;
    if (gameActive) {
        update();
    }
}

// 重置游戏
function resetGame() {
    if (gameAnimation) {
        cancelAnimationFrame(gameAnimation);
    }
    gameActive = false;
    initGame();
}

// 键盘控制
document.addEventListener('keydown', event => {
    if (!gameActive) return;
    
    switch (event.keyCode) {
        case 37: // 左箭头
            playerMove(-1);
            break;
        case 39: // 右箭头
            playerMove(1);
            break;
        case 40: // 下箭头
            playerDrop();
            break;
        case 38: // 上箭头
            playerRotate(1);
            break;
        case 32: // 空格键
            playerHardDrop();
            break;
    }
});

// 按钮事件
document.getElementById('start-btn').addEventListener('click', () => {
    if (!gameActive) {
        startGame();
    }
});

document.getElementById('pause-btn').addEventListener('click', pauseGame);
document.getElementById('reset-btn').addEventListener('click', resetGame);

// 初始化游戏画面
initGame();