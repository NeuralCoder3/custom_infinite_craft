import {
  DndContext,
  KeyboardSensor,
  Modifiers,
  MouseSensor,
  PointerActivationConstraint,
  TouchSensor,
  useDraggable,
  useSensor,
  useSensors
} from "@dnd-kit/core";
import { Coordinates } from "@dnd-kit/utilities";
import { FC, useState } from "react";
import { Axis, Draggable } from "./Draggable";
import { Wrapper } from "./Wrapper";
const defaultCoordinates = {
  x: 0,
  y: 0
};
interface Props {
  activationConstraint?: PointerActivationConstraint;
  axis?: Axis;
  handle?: boolean;
  modifiers?: Modifiers;
  buttonStyle?: React.CSSProperties;
  style?: React.CSSProperties;
  label?: string;
}

const DraggableItem: FC<DraggableItemProps> = ({
  axis,
  label,
  style,
  top,
  left,
  handle,
  buttonStyle
}) => {
  const {
    attributes,
    isDragging,
    listeners,
    setNodeRef,
    transform
  } = useDraggable({
    id: "draggable"
  });

  return (
    <Draggable
      ref={setNodeRef}
      dragging={isDragging}
      handle={handle}
      label={label}
      listeners={listeners}
      style={{ ...style, top, left }}
      buttonStyle={buttonStyle}
      transform={transform}
      axis={axis}
      {...attributes}
    />
  );
};

const DraggableStory: FC<Props> = ({
  activationConstraint,
  axis,
  handle,
  label = "Go ahead, drag me.",
  modifiers,
  style,
  buttonStyle
}) => {
//   const [{ x, y }, setCoordinates] = useState<Coordinates>(defaultCoordinates);
  const [coordinates, setCoordinates] = useState<Coordinates[]>([
    defaultCoordinates,
    { x: 100, y: 100 }
  ]);

  const mouseSensor = useSensor(MouseSensor, { activationConstraint });
  const touchSensor = useSensor(TouchSensor, {
    activationConstraint
  });
  const keyboardSensor = useSensor(KeyboardSensor, {});
  const sensors = useSensors(mouseSensor, touchSensor, keyboardSensor);
  return (
    <DndContext
      sensors={sensors}
      onDragEnd={({ delta, active, over }) => {
        console.log("delta", delta);
        console.log("active", active);
        console.log("over", over);
        // setCoordinates(({ x, y }) => {
        //   return {
        //     x: x + delta.x,
        //     y: y + delta.y
        //   };
        // });

      }}
      modifiers={modifiers}
    >
        {
            coordinates.map(({ x, y }, index) => (
      <Wrapper>
                <DraggableItem
                key={index}
                axis={axis}
                label={label}
                handle={handle}
                top={y}
                left={x}
                style={style}
                buttonStyle={buttonStyle}
                />
      </Wrapper>
            ))
        }
        {/* <DraggableItem
          axis={axis}
          label={label}
          handle={handle}
          top={y}
          left={x}
          style={style}
          buttonStyle={buttonStyle}
        /> */}
    </DndContext>
  );
};

interface DraggableItemProps {
  label: string;
  handle?: boolean;
  style?: React.CSSProperties;
  buttonStyle?: React.CSSProperties;
  axis?: Axis;
  top?: number;
  left?: number;
}

export const BasicSetup = () => <DraggableStory />;
