#
#   * *  Go3 3-player hex shaped Go game client * *
#
#  This application uses a "very thin client" approach. The coffeescript client
#  script only does three things: draw the board on a canvas element, send the
#  game point clicked to the server if user clicks on a legal move, and receive
#  from the server a new set of legal moves.


class BoardStats

  constructor: (main_object) ->
    @controller = main_object

    @row_start = [1,1,1,1,1,1,2,3,4,5,6]
    @row_end = [6,7,8,9,10,11,11,11,11,11,11]

    @w_e = [ [[1,1], [6,1]],
            [[1,2], [7,2]],
            [[1,3], [8,3]],
            [[1,4], [9,4]],
            [[1,5], [10,5]],
            [[1,6], [11,6]],
            [[2,7], [11,7]],
            [[3,8], [11,8]],
            [[4,9], [11,9]],
            [[5,10], [11,10]],
            [[6,11], [11,11]] ]

    @sw_ne = [ [[1,6], [1,1]],
              [[2,7], [2,1]],
              [[3,8], [3,1]],
              [[4,9], [4,1]],
              [[5,10], [5,1]],
              [[6,11], [6,1]],
              [[7,11], [7,2]],
              [[8,11], [8,3]],
              [[9,11], [9,4]],
              [[10,11], [10,5]],
              [[11,11], [11,6]] ]

    @nw_se = [ [[1,6], [6,11]],
              [[1,5], [7,11]],
              [[1,4], [8,11]],
              [[1,3], [9,11]],
              [[1,2], [10,11]],
              [[1,1], [11,11]],
              [[2,1], [11,10]],
              [[3,1], [11,9]],
              [[4,1], [11,8]],
              [[5,1], [11,7]],
              [[6,1], [11,6]] ]



class CanvasHelper

  constructor: () ->
    @canvas = document.getElementById('go-board')
    @context = @canvas.getContext('2d')
    @board = new BoardStats()
    @board_base = new BoardBase(this)
    @board_lines = new BoardLines(this)


  get_x: (ab) ->
    return 150 + 50*ab[0] - 25*ab[1]


  get_y: (ab) ->
    return 6 + 44*ab[1]


  get_point: (x,y) ->
    # First, use rectangular coordinates to determine which gameboard point to
    # check, then use the radius from the pixel at the center of the gameboard point
    # to see if it's close enough to map the mouse click to that point.

    point = []
    a = -1
    b = -1
    r2 = 999
    in_bounds = true
    b = Math.floor((y-28)/44)+1
    a = Math.floor((x-125+25*b)/50)
    in_bounds = false if b<1
    in_bounds = false if b>11
    in_bounds = false if a<@board.row_start[b-1]
    in_bounds = false if a>@board.row_end[b-1]
    dx = Math.abs(x-@get_x([a,b]))
    dy = Math.abs(y-@get_y([a,b]))
    r2 = dx*dx+dy*dy
    in_bounds = false if r2>530 #(if radius > 23)
    point = [a,b] if (in_bounds == true)
    return point


  draw_stone: (ab,color) ->
    @context.strokeStyle = "#000000"
    @context.lineWidth = 2
    @context.fillStyle = @get_rgb(color)
    @context.beginPath()
    @context.arc(@get_x(ab),@get_y(ab),17,0,2*Math.PI,false)
    @context.fill()
    @context.stroke()
    @context.closePath()
    @context.beginPath()
    @context.strokeStyle = "#cc9933"
    @context.arc(@get_x(ab),@get_y(ab),19,0,2*Math.PI,false)
    @context.stroke()
    @context.closePath()


  get_rgb: (color) ->
    switch color
      when "red"
        clr = "#cc3333"
      when "white"
        clr = "#f0f0f0"
      when "blue"
        clr = "#5050cc"
    return clr


  remove_stone: (ab) ->
    xx = @get_x(ab)
    yy = @get_y(ab)
    @context.beginPath()
    @context.fillStyle = "#cc9933"
    @context.arc(xx,yy,19,0,2*Math.PI,false)
    @context.fill()
    @context.closePath()
    @context.beginPath()
    @context.strokeStyle = "#000000"
    @context.lineWidth = 3
    @context.moveTo(xx-11,yy-19)
    @context.lineTo(xx+11,yy+19)
    @context.stroke()
    @context.moveTo(xx+11,yy-19)
    @context.lineTo(xx-11,yy+19)
    @context.stroke()
    @context.moveTo(xx-20,yy)
    @context.lineTo(xx+20,yy)
    @context.stroke()
    @context.closePath()


  redraw: (stones) ->
    @board_base.draw_base()
    @board_lines.draw_lines()
    for color, points of stones
      for ab in points
        @draw_stone(ab,color)



class BoardBase

  constructor: (board_canvas) ->
    @b_canvas = board_canvas
    @board = @b_canvas.board
    @draw_base()


  draw_base: () ->
    canvas = document.getElementById('go-board')
    @context = canvas.getContext('2d')
    @draw_base_hex()
    @draw_base_margin()


  draw_base_hex: () ->
    @context.strokeStyle = "#000000"
    @context.lineWidth = 5
    @context.fillStyle = "#cc9933"
    @context.beginPath()
    @context.moveTo(157,26)
    @context.lineTo(443,26)
    @context.lineTo(576,270)
    @context.lineTo(443,514)
    @context.lineTo(157,514)
    @context.lineTo(25,270)
    @context.lineTo(157,26)
    @context.fill()
    @context.stroke()
    @context.closePath()


  draw_base_margin: () ->
    @context.strokeStyle = "#000000"
    @context.lineWidth = 3
    @context.beginPath()
    @context.moveTo(163,34)
    @context.lineTo(437,34)
    @context.lineTo(567,270)
    @context.lineTo(437,506)
    @context.lineTo(163,506)
    @context.lineTo(33,270)
    @context.lineTo(163,34)
    @context.stroke()
    @context.closePath()



class BoardLines

  constructor: (board_canvas) ->
    @b_canvas = board_canvas
    @board = @b_canvas.board
    @draw_lines()

  draw_lines: () ->
    @draw_w_e_lines()
    @draw_sw_ne_lines()
    @draw_nw_se_lines()


  draw_w_e_lines: () ->
    @draw_line(@board.w_e[i][0], @board.w_e[i][1]) for i in [0..10]


  draw_sw_ne_lines: () ->
    @draw_line(@board.sw_ne[i][0],@board.sw_ne[i][1]) for i in [0..10]


  draw_nw_se_lines: () ->
    @draw_line(@board.nw_se[i][0],@board.nw_se[i][1]) for i in [0..10]


  draw_line: (beg,end) ->
    canvas = document.getElementById('go-board')
    context = canvas.getContext('2d')
    context.strokeStyle = "#000000"
    context.lineWidth = 3
    context.beginPath()
    context.moveTo(@b_canvas.get_x(beg),@b_canvas.get_y(beg))
    context.lineTo(@b_canvas.get_x(end),@b_canvas.get_y(end))
    context.stroke()
    context.closePath()



# GLOBAL level

@mousedown = (e) ->
  @canvas = document.getElementById('go-board')
  dx = @canvas.offsetLeft
  dy = @canvas.offsetTop
  px = e.pageX
  py = e.pageY
  x = px-dx
  y = py-dy
  point = @canvas_helper.get_point(x,y)
  if legal_move(point)
    @canvas_helper.draw_stone(point,"red")
    obj_out = {red_move: point, new_game: @newgame}
    msg_out = JSON.stringify(obj_out)
    xhr = new XMLHttpRequest()
    url = "/make-a-move"
    xhr.open('POST',url)
    xhr.onreadystatechange = ->
      if (xhr.readyState == 4 && xhr.status == 200)
        msg_in = xhr.responseText
        response = JSON.parse(msg_in)
        add_stones(response)
        update_legal_moves(response.legal_red_moves)
    xhr.send(msg_out)
    @newgame = "no"


legal_move = (point) ->
  return @legal_moves.some (p) -> p[0] == point[0] and p[1] == point[1]


get_init_legal_moves = () ->
  legal_moves = []
  for i in [0..10]
    for j in [@canvas_helper.board.row_start[i]..@canvas_helper.board.row_end[i]]
      pp = []
      pp[0] = j
      pp[1] = i+1
      legal_moves.push(pp)
  return legal_moves


add_stones = (response) ->
  if response.stones == undefined
    @canvas_helper.draw_stone(response.white_move, "white")
    @canvas_helper.draw_stone(response.blue_move, "blue")
  else
    stones = JSON.parse(response.stones)
    reset(stones)


reset = (stones) ->
  @canvas_helper.redraw(stones)


update_legal_moves = (legal_moves) ->
  @legal_moves = legal_moves


start = () ->
  @newgame = "yes"
  @canvas_helper = new CanvasHelper
  @legal_moves = get_init_legal_moves()



window.onload = start
