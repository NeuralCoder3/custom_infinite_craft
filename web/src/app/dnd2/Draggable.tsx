import React from "react";
import { useDraggable, useDroppable } from "@dnd-kit/core";
import { Note } from "./interfaces";
import * as API from "./api";

const CustomStyle = {
  // display: "flex",
  width: "120px",
  // height: "140px",
  minHeight: "140px",
  backgroundColor: "#e8e8a2",
};

interface DraggableProps {
  id: string;
  note: Note,
  styles: object;
}

export function Draggable({ id, note, styles }: DraggableProps) {
  const { attributes, listeners, setNodeRef, transform } = useDraggable({
    id
  });

  const { isOver, setNodeRef:setDroppableNodeRef } = useDroppable({
    id
  });

  const style = transform
    ? {
        transform: `translate3d(${transform.x}px, ${transform.y}px, 0)`
      }
    : {};

  const text = note.content ? note.content : "Loading...";
  const image = note.image ? 
    <img width="120px" height="120px" src={API.IMAGE_URL+note.image} alt="" /> :
    null;

  return (
    <div
      // ref={setNodeRef}
      ref={(node) => {
        setNodeRef(node);
        setDroppableNodeRef(node);
      }}
      style={{ ...style, ...CustomStyle, ...styles }}
      {...listeners}
      {...attributes}
    >
      {/* 
      title text centered 
      below the image on a new line
       */}
      {image}
      {/* <div>{text} ({id})</div> */}
      <div>{text}</div>
    </div>
  );
}
