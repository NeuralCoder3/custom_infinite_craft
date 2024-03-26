import React, { useEffect, useState } from "react";
import { DndContext } from "@dnd-kit/core";
import { Draggable } from "./Draggable";
import * as API from "./api";
import "./styles.css";
import { Note } from "./interfaces";
import useLocalStorageState from "use-local-storage-state";

const notesData: Note[] = [
  {
    id: "1",
    content: "water",
    image: "images/water.png",
    position: {
      x: 0,
      y: 0
    }
  },
  {
    id: "2",
    content: "fire",
    image: "images/fire.png",
    position: {
      x: 0,
      y: 140
    }
  },
  {
    id: "3",
    content: "earth",
    image: "images/earth.png",
    position: {
      x: 0,
      y: 280
    }
  }
];

export function App() {
  const [notes, setNotes] = useLocalStorageState("note", {defaultValue: notesData});
  const [key_count, setKeyCount] = useState(1 + notesData.map((x) => parseInt(x.id)).reduce((a, b) => Math.max(a, b)));
  const [foundElements, setFoundElements] = useLocalStorageState<string[]>("foundElements",
    {defaultValue: notesData.map((x) => x.content!) as string[]}
  );

  useEffect(() => {
    setKeyCount(1+notes.reduce((a, b) => Math.max(a, parseInt(b.id)), 0));
  }, [notes, key_count]);

  const [subtract, setSubtract] = useLocalStorageState<boolean>("subtract", {defaultValue: false});


  const addNote = (content: string | null, x: number, y: number, additionalData={}) => {
      const new_key = `${key_count}`;
      const new_note: Note = {
        ...additionalData,
        id: new_key,
        content: content,
        position: {
          x: x,
          y: y
        }
      };
      setNotes((prev) => [...prev, new_note]);
      return new_note;
  };


  async function handleDragEnd(ev: any) {
    const note = notes.find((x) => x.id === ev.active.id)!;
    const new_x = note.position.x + ev.delta.x;
    const new_y = note.position.y + ev.delta.y;
    setNotes((notes) => {
      return notes.map((x) => {
        if (x.id === ev.active.id) {
          return {
            ...x,
            position: {
              x: new_x,
              y: new_y
            }
          };
        }
        return x;
      });
    });

    if (ev.over && ev.over.id !== ev.active.id) {
      const other_note = notes.find((x) => x.id === ev.over.id)!;
      const element2 = note.content;
      const element1 = other_note.content;
      if (!element1 || !element2) {
        console.log("invalid elements");
        return;
      }
      console.log(`Combining ${element1} and ${element2} ...`);

      const new_note = addNote(null, 
        (new_x + other_note.position.x) / 2, 
        (new_y + other_note.position.y) / 2);

      API.combinePost(element1, element2, false, subtract).then((combined) => {
        console.log("Result: ", combined);
        console.log(`${element1} + ${element2} = ${combined.combined}`);
        setNotes((prev) =>
          prev.map((x) => {
            if (x.id === new_note.id) {
              return {
                ...x,
                content: combined.combined,
                image: "images/generating.png"
              };
            }
            return x;
          }
        ));
        setFoundElements((prev) => {
          if (prev.includes(combined.combined)) {
            return prev;
          }
          return [...prev, combined.combined];
        });
        API.combinePost(element1, element2, true, subtract).then((combined) => {
          setNotes((prev) =>
            prev.map((x) => {
              if (x.content === combined.combined) {
                return {
                  ...x,
                  image: combined.image,
                };
              }
              return x;
            }
          ));
        });
      });

      setNotes((notes) => notes.filter((x) => x.id !== note.id && x.id !== other_note.id));
    }
  }

  function doubleClickHandler(ev: any) {
    // duplicate note
    if (!ev.id) return;
    console.log(ev);
    const note = notes.find((x) => x.id === ev.id)!;
    if (!note.content) {
      console.log("invalid note");
      return;
    }
    addNote(note.content, note.position.x + 50, note.position.y + 50, {image: note.image});
  }

  function rightClickHandler(ev: any) {
    // remove note
    const note = notes.find((x) => x.id === ev.id)!;
    if (!note.content) {
      console.log("invalid note");
      return;
    }
    setNotes(notes.filter((x) => x.id !== ev.id));
  }

  const image_url = (element: string) => "images/" + element.toLowerCase().replaceAll(" ", "_") + ".png";

  const addElement = (element: string) => {
    // center of screen +- random offset as int
    const x = Math.floor(window.innerWidth / 2 + Math.random() * 100 - 50);
    const y = Math.floor(window.innerHeight / 2 + Math.random() * 100 - 50);
    addNote(element, x, y, {image: image_url(element)});
  }

  const sidebar = (
    <div>
      <h3> {foundElements.length} Elements </h3>
      {foundElements.map((element) => (
        <div key={element}>
          <button 
            style={{ width: "100%" }}
            onClick={() => addElement(element)}
          >{element}</button>
        </div>
      ))}
    </div>
  );

  const canvas = (
    <DndContext onDragEnd={handleDragEnd}>
      {notes.map((note) => (
        <div 
          key={note.id} 
          onDoubleClick={() => doubleClickHandler({ id: note.id })}
          onContextMenu={(ev) => {
            ev.preventDefault();
            rightClickHandler({ id: note.id });
          }}
        >
          <Draggable
            styles={{
              position: "absolute",
              left: `${note.position.x}px`,
              top: `${note.position.y}px`
            }}
            key={note.id}
            id={note.id}
            note={note}
          />
        </div>
      ))}
    </DndContext>
  );

  const settings = (
    <div>
      <input  
        type="checkbox" 
        checked={subtract} 
        onChange={(ev) => setSubtract(ev.target.checked)}
      />
      <label>Subtract</label>
    </div>
  );

  return (
    <div>
      {/* 
        at top the settings
        at the right the sidebar (25% of screen) 
        at the left the canvas (75% of screen)
      */}
      {settings}
      <div style={{ display: "flex" }}>
        <div style={{ width: "80%" }}>
          {canvas}
        </div>
        <div style={{ width: "20%" }}>
          {sidebar}
        </div>
      </div>
    </div>
  );
}
