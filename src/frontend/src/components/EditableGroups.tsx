import React, { useState } from 'react';
import { DragDropContext, Droppable, Draggable, DropResult } from 'react-beautiful-dnd';
import '../stylesheets/EditableGroups.css';

interface Group {
  name: string;
  members: string[];
}

interface EditableGroupsProps {
  initialGroups: Group[];
  onSave: (groups: Group[]) => void;
}

const EditableGroups: React.FC<EditableGroupsProps> = ({ initialGroups, onSave }) => {
  const [groups, setGroups] = useState<Group[]>(initialGroups);

  // Handle the end of a drag event
  const handleDragEnd = (result: DropResult) => {
    if (!result.destination) return;

    const { source, destination } = result;

    // Extract group indices from droppableIds
    const sourceGroupIndex = parseInt(source.droppableId.split('-')[1], 10);
    const destinationGroupIndex = parseInt(destination.droppableId.split('-')[1], 10);

    const sourceGroup = groups[sourceGroupIndex];
    const destinationGroup = groups[destinationGroupIndex];

    const sourceItems = Array.from(sourceGroup.members);
    const destinationItems = Array.from(destinationGroup.members);

    // Remove dragged item from source
    const [movedItem] = sourceItems.splice(source.index, 1);

    // Add dragged item to destination
    destinationItems.splice(destination.index, 0, movedItem);

    const updatedGroups = [...groups];
    updatedGroups[sourceGroupIndex] = {
      ...sourceGroup,
      members: sourceItems,
    };
    updatedGroups[destinationGroupIndex] = {
      ...destinationGroup,
      members: destinationItems,
    };

    setGroups(updatedGroups);
    onSave(updatedGroups);
  };

  return (
    <DragDropContext onDragEnd={handleDragEnd}>
      <div className="csv-preview">
        <h2>CSV Preview</h2>
        <div className="csv-table">
          <div className="csv-table-header">
            <div className="csv-table-row">
              <div className="csv-table-cell">Group Name</div>
              <div className="csv-table-cell">Student Names</div>
            </div>
          </div>
          <div className="csv-table-body">
            {groups.map((group, groupIndex) => (
              <div className="csv-table-row" key={`group-${groupIndex}`}>
                <div className="csv-table-cell">{group.name}</div>
                <div className="csv-table-cell">
                  <Droppable droppableId={`group-${groupIndex}`} direction="horizontal">
                    {(provided) => (
                      <div
                        className="group-members-container"
                        ref={provided.innerRef}
                        {...provided.droppableProps}
                      >
                        {group.members.map((member, memberIndex) => (
                          <Draggable
                            key={`member-${groupIndex}-${memberIndex}`}
                            draggableId={`member-${groupIndex}-${memberIndex}`}
                            index={memberIndex}
                          >
                            {(provided) => (
                              <div
                                ref={provided.innerRef}
                                {...provided.draggableProps}
                                {...provided.dragHandleProps}
                                className="group-member"
                              >
                                {member}
                              </div>
                            )}
                          </Draggable>
                        ))}
                        {provided.placeholder}
                      </div>
                    )}
                  </Droppable>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </DragDropContext>
  );
};

export default EditableGroups;
