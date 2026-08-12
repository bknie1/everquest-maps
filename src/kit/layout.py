"""Layout hierarchy for a zone. One source of truth for every boundary, so shading,
grid, margin and frame can never disagree.

    frame  ⊃  margin  ⊃  grid  ⊃  content

- content : the base geometry's own extent. Nothing about it is invented.
- grid    : content plus a breathing gap, so the map never touches the grid.
            GRID is the parent of content: margin decoration stops at the grid,
            never at the content, or the border motif bleeds into the grid.
- margin  : where decoration lives — shading, doodles, compass, title.
- frame   : the drawn border, outermost.

Shading is bounded by GRID and nothing else, which is what stops it being cut
short on one side by a value chosen somewhere unrelated, and stops the margin
motif bleeding inside the grid.
"""
GAP     = 0.055   # content -> grid
MARGIN  = 0.150   # grid    -> margin, sides and bottom
MARG_T  = 0.240   # grid    -> margin, top (the title lives here)
FRAME   = 0.020   # margin  -> frame

def layout(content, top_extra=0.0):
    """content = (x0,x1,y0,y1) of the base geometry."""
    x0, x1, y0, y1 = content
    S = max(x1 - x0, y1 - y0)
    g  = (x0 - S*GAP, x1 + S*GAP, y0 - S*GAP, y1 + S*GAP)
    m  = (g[0] - S*MARGIN, g[1] + S*MARGIN,
          g[2] - S*(MARG_T + top_extra), g[3] + S*MARGIN)
    f  = (m[0] - S*FRAME, m[1] + S*FRAME, m[2] - S*FRAME, m[3] + S*FRAME)
    return {'S': S, 'content': content, 'grid': g, 'margin': m, 'frame': f,
            'title_band': (g[0], g[1], m[2] + S*0.03, g[2] - S*0.03)}
