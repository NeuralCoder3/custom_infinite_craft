import update from 'immutability-helper'
import type { CSSProperties, FC } from 'react'
import { createRef, useCallback, useRef, useState } from 'react'
import type { XYCoord } from 'react-dnd'
import { useDrop } from 'react-dnd'

import { Box } from './Box'
import type { DragItem } from './interfaces'
import { ItemTypes } from './ItemTypes'

const styles: CSSProperties = {
  width: 400,
  height: 400,
  border: '1px solid black',
  position: 'relative',
}

export interface ContainerState {
  boxes: { [key: string]: { top: number; left: number; title: string } }
}

export const Container = () => {
  const [boxes, setBoxes] = useState<{
    [key: string]: {
      top: number
      left: number
      title: string
      ref: React.MutableRefObject<HTMLDivElement|undefined>
    }
  }>({
    a: { top: 20, left: 80, title: 'Drag me around', ref: useRef() },
    b: { top: 180, left: 20, title: 'Drag me too', ref: useRef() },
  })

  const moveBox = useCallback(
    (id: string, left: number, top: number) => {
      setBoxes(
        update(boxes, {
          [id]: {
            $merge: { left, top },
          },
        }),
      )
    },
    [boxes, setBoxes],
  )
    

  const [, drop] = useDrop(
    () => ({
      accept: ItemTypes.BOX,
      drop(item: DragItem, monitor) {
        const delta = monitor.getDifferenceFromInitialOffset() as XYCoord
        const left = Math.round(item.left + delta.x)
        const top = Math.round(item.top + delta.y)
        moveBox(item.id, left, top)
        // console.log("dropped");
        // check for overlap
        for (let key in boxes) {
          if (key !== item.id) {
            const box = boxes[key]
            if (
              left > box.left - 50 &&
              left < box.left + 50 &&
              top > box.top - 50 &&
              top < box.top + 50
            ) {
              console.log('overlap')
            }
          }
        }
        return undefined
      },
    }),
    [moveBox],
  )

  return (
    <div ref={drop} style={styles}>
      {Object.keys(boxes).map((key) => {
        const { left, top, title, ref } = boxes[key] as {
          top: number
          left: number
          title: string
          ref: React.MutableRefObject<HTMLDivElement>
        }
        return (
          <Box
            key={key}
            id={key}
            left={left}
            top={top}
            ref={ref}
          >
            {title}
          </Box>
        )
      })}
    </div>
  )
}
