import React from "react";
import { useDraggable, useDroppable } from "@dnd-kit/core";

const CustomStyle = {
  display: "flex",
  width: "140px",
  height: "140px",
  backgroundColor: "#e8e8a2"
};

export function Draggable({ id, content, styles }) {
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
      {content}
    </div>
  );
}
