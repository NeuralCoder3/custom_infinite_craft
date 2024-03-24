import React, { useState } from "react";
import { DndContext, useDraggable } from "@dnd-kit/core";
import { Draggable } from "./Draggable";
import * as API from "./api";
import "./styles.css";
import { Note } from "./interfaces";

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
  const [notes, setNotes] = useState(notesData);
  const [key_count, setKeyCount] = useState(1 + notesData.map((x) => parseInt(x.id)).reduce((a, b) => Math.max(a, b)));
  // use local storage here
  const [foundElements, setFoundElements] = useState<string[]>(
    notesData.map((x) => x.content!)
  );

  const [subtract, setSubtract] = useState(false);

  async function handleDragEnd(ev: any) {
    const note = notes.find((x) => x.id === ev.active.id)!;
    note.position.x += ev.delta.x;
    note.position.y += ev.delta.y;
    let _notes = notes.map((x) => {
      if (x.id === note.id) return note;
      return x;
    });

    if (ev.over && ev.over.id !== ev.active.id) {
      // console.log("over: ", ev.over.id);
      const other_note = notes.find((x) => x.id === ev.over.id)!;
      const element2 = note.content;
      const element1 = other_note.content;
      if (!element1 || !element2) {
        console.log("invalid elements");
        return;
      }
      console.log(`Combining ${element1} and ${element2} ...`);
      const new_key = `${key_count}`;
      const new_note: Note = {
        id: new_key,
        content: null,
        position: {
          x: (note.position.x + other_note.position.x) / 2,
          y: (note.position.y + other_note.position.y) / 2
        }
      };
      // API.combinePost(element1, element2).then((combined) => {
      //   console.log("Result: ", combined);
      //   console.log(`${element1} + ${element2} = ${combined.combined}`);
      //   // new_note.content = combined.combined;
      //   // new_note.image = combined.image;
      //   setNotes((prev) =>
      //     prev.map((x) => {
      //       if (x.id === new_key) {
      //         return {
      //           ...x,
      //           content: combined.combined,
      //           image: combined.image
      //         };
      //       }
      //       return x;
      //     }
      //   ));
      //   setFoundElements((prev) => {
      //     if (prev.includes(combined.combined)) {
      //       return prev;
      //     }
      //     return [...prev, combined.combined];
      //   });
      // });
      API.combinePost(element1, element2, false, subtract).then((combined) => {
        console.log("Result: ", combined);
        console.log(`${element1} + ${element2} = ${combined.combined}`);
        setNotes((prev) =>
          prev.map((x) => {
            if (x.id === new_key) {
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
              if (x.id === new_key) {
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




      // const combined = await API.combinePost(element1, element2);
      // console.log(`${element1} + ${element2} = ${combined.combined}`);
      // // add new note
      // const newNote = {
      //     id: `${key_count}`,
      //     content: combined.combined,
      //     position: {
      //         x: (note.position.x + other_note.position.x) / 2,
      //         y: (note.position.y + other_note.position.y) / 2
      //     }
      // };

      // filter out old notes
      // _notes = [..._notes, newNote];
      _notes = _notes.filter((x) => x.id !== note.id && x.id !== other_note.id);
      _notes.push(new_note);
      setKeyCount(key_count + 1);
    }
    setNotes(_notes);
  }

  function doubleClickHandler(ev: any) {
    // duplicate note
    if (!ev.id) return;
    console.log(ev);
    // clone ev.id
    const note = notes.find((x) => x.id === ev.id)!;
    if (!note.content) {
      console.log("invalid note");
      return;
    }
    const newNote = {
      ...note,
      id: `${key_count}`,
      position: {
        x: note.position.x + 50,
        y: note.position.y + 50
      }
    };
    setNotes([...notes, newNote]);
    setKeyCount(key_count + 1);
  }

  function rightClickHandler(ev: any) {
    // remove note
    // if (!ev.id) return;
    const note = notes.find((x) => x.id === ev.id)!;
    if (!note.content) {
      console.log("invalid note");
      return;
    }
    setNotes(notes.filter((x) => x.id !== ev.id));
  }

  return (
    <div>
      <input  
        type="checkbox" 
        checked={subtract} 
        onChange={(ev) => setSubtract(ev.target.checked)}
      />
      <label>Subtract</label>
    <br />
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
    </div>
  );
}
