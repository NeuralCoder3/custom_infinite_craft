import React, { useState } from "react";
import { DndContext, useDraggable } from "@dnd-kit/core";
import { Draggable } from "./Draggable";
import { Droppable } from "./Droppable";
import "./styles.css";

const notesData = [
  {
    id: "1",
    content: "Study English 1",
    position: {
      x: 0,
      y: 0
    }
  },
    {
        id: "2",
        content: "Study Math 2",
        position: {
        x: 0,
        y: 100
        }
    },
    {
        id: "3",
        content: "Study Science 3",
        position: {
        x: 0,
        y: 200
        }
    }
];

export function App() {
  const [notes, setNotes] = useState(notesData);

  function handleDragEnd(ev:any) {
    console.log("over: ", ev.over);
    // What to do here??
    // It's not a sortable, it's a free drag and drop
    const note = notes.find((x) => x.id === ev.active.id)!;
    note.position.x += ev.delta.x;
    note.position.y += ev.delta.y;
    const _notes = notes.map((x) => {
      if (x.id === note.id) return note;
      return x;
    });
    setNotes(_notes);
  }

  return (
    <DndContext onDragEnd={handleDragEnd}>
      {/* <Droppable> */}
        {notes.map((note) => (
          <Draggable
            styles={{
              position: "absolute",
              left: `${note.position.x}px`,
              top: `${note.position.y}px`
            }}
            key={note.id}
            id={note.id}
            content={note.content}
          />
        ))}
      {/* </Droppable> */}
    </DndContext>
  );
}
