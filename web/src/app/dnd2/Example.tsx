import React, { useState } from "react";
import { DndContext, useDraggable } from "@dnd-kit/core";
import { Draggable } from "./Draggable";
import * as API from "./api";
import "./styles.css";

const notesData = [
  {
    id: "1",
    content: "water",
    position: {
      x: 0,
      y: 0
    }
  },
    {
        id: "2",
        content: "fire",
        position: {
        x: 0,
        y: 100
        }
    },
    {
        id: "3",
        content: "earth",
        position: {
        x: 0,
        y: 200
        }
    }
];

export function App() {
  const [notes, setNotes] = useState(notesData);
  const [key_count, setKeyCount] = useState(1+notesData.map((x) => parseInt(x.id)).reduce((a, b) => Math.max(a, b)));

  async function handleDragEnd(ev:any) {
    const note = notes.find((x) => x.id === ev.active.id)!;
    note.position.x += ev.delta.x;
    note.position.y += ev.delta.y;
    let _notes = notes.map((x) => {
      if (x.id === note.id) return note;
      return x;
    });

    if (ev.over && ev.over.id !== ev.active.id) {
        console.log("over: ", ev.over.id);
        const other_note = notes.find((x) => x.id === ev.over.id)!;
        const element1 = note.content;
        const element2 = other_note.content;
        console.log(`Combining ${element1} and ${element2} ...`);
        const combined = await API.combinePost(element1, element2);
        console.log(`${element1} + ${element2} = ${combined.combined}`);
        // add new note
        const newNote = {
            id: `${key_count}`,
            content: combined.combined,
            position: {
                x: (note.position.x + other_note.position.x) / 2,
                y: (note.position.y + other_note.position.y) / 2
            }
        };
        // filter out old notes
        // _notes = [..._notes, newNote];
        _notes = _notes.filter((x) => x.id !== note.id && x.id !== other_note.id);
        _notes.push(newNote);
        setKeyCount(key_count+1);
    }
    setNotes(_notes);
  }

  function doubleClickHandler(ev:any) {
    console.log(ev);
    // clone ev.id
    const note = notes.find((x) => x.id === ev.id)!;
    const newNote = {
        id: `${key_count}`,
        content: note.content,
        position: {
            x: note.position.x + 50,
            y: note.position.y + 50
        }
    };
    setNotes([...notes, newNote]);
    setKeyCount(key_count+1);
  }

  return (
    <DndContext onDragEnd={handleDragEnd}>
        {notes.map((note) => (
            <div key={note.id} onDoubleClick={() => doubleClickHandler({id: note.id})}>
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
            </div>
        ))}
    </DndContext>
  );
}
