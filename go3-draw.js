// Board geometry constants
const ROW_START = [1, 1, 1, 1, 1, 1, 2, 3, 4, 5, 6];
const ROW_END = [6, 7, 8, 9, 10, 11, 11, 11, 11, 11, 11];
const W_E = [
    [[1, 1], [6, 1]],
    [[1, 2], [7, 2]],
    [[1, 3], [8, 3]],
    [[1, 4], [9, 4]],
    [[1, 5], [10, 5]],
    [[1, 6], [11, 6]],
    [[2, 7], [11, 7]],
    [[3, 8], [11, 8]],
    [[4, 9], [11, 9]],
    [[5, 10], [11, 10]],
    [[6, 11], [11, 11]],
];
const SW_NE = [
    [[1, 6], [1, 1]],
    [[2, 7], [2, 1]],
    [[3, 8], [3, 1]],
    [[4, 9], [4, 1]],
    [[5, 10], [5, 1]],
    [[6, 11], [6, 1]],
    [[7, 11], [7, 2]],
    [[8, 11], [8, 3]],
    [[9, 11], [9, 4]],
    [[10, 11], [10, 5]],
    [[11, 11], [11, 6]],
];
const NW_SE = [
    [[1, 6], [6, 11]],
    [[1, 5], [7, 11]],
    [[1, 4], [8, 11]],
    [[1, 3], [9, 11]],
    [[1, 2], [10, 11]],
    [[1, 1], [11, 11]],
    [[2, 1], [11, 10]],
    [[3, 1], [11, 9]],
    [[4, 1], [11, 8]],
    [[5, 1], [11, 7]],
    [[6, 1], [11, 6]],
];
// Coordinate transform functions
function getX(ab) { return 150 + 50 * ab[0] - 25 * ab[1]; }
function getY(ab) { return 6 + 44 * ab[1]; }
// Drawing helper functions
function drawBaseHex(ctx) {
    ctx.strokeStyle = "#000000";
    ctx.lineWidth = 5;
    ctx.fillStyle = "#cc9933";
    ctx.beginPath();
    ctx.moveTo(157, 26);
    ctx.lineTo(443, 26);
    ctx.lineTo(576, 270);
    ctx.lineTo(443, 514);
    ctx.lineTo(157, 514);
    ctx.lineTo(25, 270);
    ctx.lineTo(157, 26);
    ctx.fill();
    ctx.stroke();
    ctx.closePath();
}
function drawBaseMargin(ctx) {
    ctx.strokeStyle = "#000000";
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(163, 34);
    ctx.lineTo(437, 34);
    ctx.lineTo(567, 270);
    ctx.lineTo(437, 506);
    ctx.lineTo(163, 506);
    ctx.lineTo(33, 270);
    ctx.lineTo(163, 34);
    ctx.stroke();
    ctx.closePath();
}
function drawLine(ctx, beg, end) {
    ctx.strokeStyle = "#000000";
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(getX(beg), getY(beg));
    ctx.lineTo(getX(end), getY(end));
    ctx.stroke();
    ctx.closePath();
}
function drawLines(ctx) {
    for (const [beg, end] of W_E)
        drawLine(ctx, beg, end);
    for (const [beg, end] of SW_NE)
        drawLine(ctx, beg, end);
    for (const [beg, end] of NW_SE)
        drawLine(ctx, beg, end);
}
// Main exported function
export function draw(canvas) {
    const ctx = canvas.getContext('2d');
    drawBaseHex(ctx);
    drawBaseMargin(ctx);
    drawLines(ctx);
}
