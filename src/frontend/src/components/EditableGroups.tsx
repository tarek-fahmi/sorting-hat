import React, { useState, ReactNode } from 'react';
import { DndProvider, useDrag, useDrop } from 'react-dnd';
import { HTML5Backend } from 'react-dnd-html5-backend';
import '../stylesheets/EditableGroups.css';

interface Group {
  name: string;
  members: string[];
}

interface EditableGroupsProps {
  initialGroups: Group[];
  onSave: (groups: Group[]) => void;
}

interface DraggableItem {
  member: string;
  groupIndex: number;
  memberIndex: number;
}

const EditableGroups: React.FC<EditableGroupsProps> = ({ initialGroups, onSave }) => {
  const [groups, setGroups] = useState<Group[]>(initialGroups);

  const moveMember = (source: DraggableItem, destinationGroupIndex: number, destinationMemberIndex: number) => {
    const updatedGroups = [...groups];
    const sourceGroup = updatedGroups[source.groupIndex];
    const destinationGroup = updatedGroups[destinationGroupIndex];

    // Remove member from source group
    const [movedMember] = sourceGroup.members.splice(source.memberIndex, 1);

    // Add member to destination group
    destinationGroup.members.splice(destinationMemberIndex, 0, movedMember);

    setGroups(updatedGroups);
    onSave(updatedGroups);
  };

  const Member: React.FC<{ member: string; groupIndex: number; memberIndex: number }> = ({ member, groupIndex, memberIndex }) => {
    const [, dragRef] = useDrag({
      type: 'MEMBER',
      item: { member, groupIndex, memberIndex },
    });

    return (
      <div ref={dragRef} className="group-member">
        {member}
      </div>
    );
  };

  const GroupDropArea: React.FC<{ groupIndex: number; memberIndex: number; children: ReactNode }> = ({ groupIndex, memberIndex, children }) => {
    const [, dropRef] = useDrop({
      accept: 'MEMBER',
      drop: (item: DraggableItem) => {
        moveMember(item, groupIndex, memberIndex);
      },
    });

    return (
      <div ref={dropRef} className="drop-area">
        {children}
      </div>
    );
  };

  return (
    <DndProvider backend={HTML5Backend}>
      <div className="csv-preview">
        <h2>CSV Preview</h2>
        <table className="csv-table">
          <thead>
            <tr>
              <th>Group Name</th>
              <th>Student Names</th>
            </tr>
          </thead>
          <tbody>
            {groups.map((group, groupIndex) => (
              <tr key={groupIndex}>
                <td>{group.name}</td>
                <td>
                  <div className="group-members-container">
                    {group.members.map((member, memberIndex) => (
                      <GroupDropArea key={memberIndex} groupIndex={groupIndex} memberIndex={memberIndex}>
                        <Member member={member} groupIndex={groupIndex} memberIndex={memberIndex} />
                      </GroupDropArea>
                    ))}
                    <GroupDropArea groupIndex={groupIndex} memberIndex={group.members.length}>
                      <div className="add-member-placeholder">Drop here</div>
                    </GroupDropArea>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </DndProvider>
  );
};

export default EditableGroups;
