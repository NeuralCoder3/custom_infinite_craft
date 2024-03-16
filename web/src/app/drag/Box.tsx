import type { CSSProperties, FC, ReactNode } from 'react'
import { useDrag } from 'react-dnd'

import { ItemTypes } from './ItemTypes'

const style: CSSProperties = {
  position: 'absolute',
  border: '1px dashed gray',
  backgroundColor: 'white',
  padding: '0.5rem 1rem',
  cursor: 'move',
}

export interface BoxProps {
  id: any
  left: number
  top: number
  children?: ReactNode
  ref: React.MutableRefObject<HTMLDivElement|null>
}

export const Box: FC<BoxProps> = ({
  id,
  left,
  top,
  children,
  ref
}) => {
  const [{ isDragging }, drag] = useDrag(
    () => ({
      type: ItemTypes.BOX,
      item: { id, left, top },
      collect: (monitor) => ({
        isDragging: monitor.isDragging(),
      }),
    }),
    [id, left, top],
  )

  if (isDragging) {
    return <div ref={drag} />
  }
  return (
    <div
      className="box"
      ref={(node) => {drag(node); ref.current = node}}
      style={{ ...style, left, top }}
      data-testid="box"
    >
      {children}
    </div>
  )
}
