"use strict";

const numRows = 30;
const numColumns = 30;
const numBlocks = numRows*numColumns;
const testGrid = document.getElementById('test-grid');
testGrid.style.width = screen.width +"px";
testGrid.style.height = screen.height + "px";
testGrid.style.grid =
    `repeat(${numRows}, 1fr) / repeat(${numColumns}, 1fr)`;
const rectangles = []
for (let i = 0; i < numBlocks; i++) {
  const div = document.createElement('div');
  div.id = `block-${i}`;
  div.classList.add("state-untested");
  div.innerText = i;
  testGrid.appendChild(div);
  const rectangle = div.getBoundingClientRect();
  rectangles.push(rectangle);
}
const canvas = document.getElementById("test-canvas");
canvas.width = screen.width;
canvas.height = screen.height;
const ctx = canvas.getContext("2d");
ctx.strokeStyle = "red";
ctx.lineWidth = 1;

// Begin a Path
const point1 = {x: 700, y:500};
const point2 = {x: 800, y:200};
ctx.beginPath();
ctx.moveTo(point1.x,point1.y);
ctx.lineTo(point2.x,point2.y);
ctx.lineWidth= 1;
ctx.stroke();
check();
point1.x = 800;
point1.y = 100;
point2.x = 1000;
point2.y = 700;
ctx.beginPath();
ctx.moveTo(point1.x,point1.y);
ctx.lineTo(point2.x,point2.y);
ctx.lineWidth= 1;
ctx.stroke();
check();


function checkLineRectIntersection(point1, point2, rectangle) {
  const x1 = point1.x;
  const y1 = point1.y;
  const x2 = point2.x;
  const y2 = point2.y;

  const rectTopLeftX = rectangle.x;
  const rectTopLeftY = rectangle.y;
  const rectBottomRightX = rectTopLeftX + rectangle.width;
  const rectBottomRightY = rectTopLeftY + rectangle.height;

  const dx = x2 - x1;
  const dy = y2 - y1;

  const rectMinX = Math.min(rectTopLeftX, rectBottomRightX);
  const rectMaxX = Math.max(rectTopLeftX, rectBottomRightX);
  const rectMinY = Math.min(rectTopLeftY, rectBottomRightY);
  const rectMaxY = Math.max(rectTopLeftY, rectBottomRightY);

  if (x1 < rectMinX && x2 < rectMinX) {
      return false;
  }
  if (x1 > rectMaxX && x2 > rectMaxX) {
      return false;
  }

  if (y1 < rectMinY && y2 < rectMinY) {
      return false;
  }
  if (y1 > rectMaxY && y2 > rectMaxY) {
      return false;
  }

  const lineNormalX = -dy;
  const lineNormalY = dx;

  const rectCenterX = (rectMinX + rectMaxX) / 2;
  const rectCenterY = (rectMinY + rectMaxY) / 2;

  const rectHalfWidth = (rectMaxX - rectMinX) / 2;
  const rectHalfHeight = (rectMaxY - rectMinY) / 2;

  const separation = Math.abs((x2 - rectCenterX) * lineNormalX + (y2 - rectCenterY) * lineNormalY);

  const projectedHalfWidth = rectHalfWidth * Math.abs(lineNormalX) + rectHalfHeight * Math.abs(lineNormalY);

  return separation <= projectedHalfWidth;
}



function check()
{
  for(let i=0;i<rectangles.length;i++)
  {
    var rectangle = rectangles[i];
    if(checkLineRectIntersection(point1, point2, rectangle))
    {
      const div = document.getElementById(`block-${i}`);
      div.classList.add("state-tested");
    }
  }
}
// var count = 1;
// function update(){
//   point1.x = point2.x;
//   point1.y = point2.y;
//   point2.x += (count*7+20);
//   point2.y += (count*2+43);
//   count++;
//   ctx.beginPath();
//   ctx.moveTo(point1.x,point1.y);
//   ctx.lineTo(point2.x,point2.y);
//   ctx.lineWidth= 1;
//   ctx.stroke();
//   check();
//   if(count == 10){
//     count = -10;
//   }

//   // if(count == 10){
//   //   count = -100;
//   // }
// }

// const test = setInterval(update,100);
