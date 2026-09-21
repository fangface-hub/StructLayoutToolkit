# StructLayoutToolkit User Guide

StructLayoutToolkit provides tools for viewing and editing binary files and
reassembled packet payloads. Files are initially opened from your Documents
folder. After you open or save a file, the application remembers the last used
folder for that type of file.

## Launcher Window

The launcher opens each editor in a separate process. Closing the launcher does
not close editors that are already open.

- **Binary Editor** opens the Binary Viewer.
- **Packet Data Editor** opens the Packet Data Editor.

You can open more than one editor at a time.

## Binary Viewer Window

Use the Binary Viewer to inspect and modify a binary file either as raw bytes or
as fields decoded by a StructLayout definition.

### Binary editing workflow

1. To work with structured data, select **Type Definition > Open
   StructLayout...** or load the built-in PCAP or PCAPNG layout from **Type
   Definition > Load Resource**.
2. Select **File > Open Binary...** and choose a binary file. If necessary,
   select the root structure used to decode it.
3. Edit values in the table.
4. Select **File > Save Binary** or **Save Binary As...** to encode and save the
   current data.

Use **File > New Binary...** to create a zero-filled binary value. When a
structure is selected, its minimum required size is used. Without a structure,
the viewer opens in raw binary mode.

### Data table

The table displays offset, hexadecimal bytes, field name, type, value, and size.
Nested structures can be expanded and collapsed.

- In raw binary mode, edit the **hex** cells. Enter exactly the number of bytes
  shown in that row, using hexadecimal digits with optional spaces.
- In structured mode, edit the **value** cells. Press Enter or move focus away
  from the cell to apply the value.
- Right-click the **hex** cell of a `bytearray` field and select **Open
  BinaryEditorWindow** to edit that field in a nested Binary Viewer. Use
  **Return with saving** to apply the nested edits or **Return without saving**
  to discard them.
- Change **Bytes/row** to control how raw bytes are grouped.
- Select **Re-decode** after changing definitions to decode the current bytes
  again.

If a value cannot be converted to the field type or the structure cannot be
encoded, an error dialog is shown and the file is not saved.

### File menu

- **Save Binary** writes changes to the current binary file.
- **Save Binary As...** writes the encoded data to another file.
- **Export to CSV...** exports a flat list containing each field's nesting
  level and path.
- **Export to JSON...** exports the displayed field tree as nested JSON.
- **Exit** closes the Binary Viewer.

### Type Definition menu

- **Open StructLayout...** loads structure and enum definitions from JSON.
- **Load Resource > PCAP**, **PCAPNG**, **PE**, and **ELF** load built-in layouts.
  **PE** is for Windows executable files, and **ELF** is for Linux executable
  files.
- **Save StructLayout** and **Save StructLayout As...** save the active layout.
- **Select Struct...** selects the root structure and re-decodes the data.
- **Struct Definitions...** opens the StructDef Dict Editor.
- **Enum Definitions...** opens the EnumDef Dict Editor.

## Packet Data Editor Window

Use the Packet Data Editor to open a PCAP or PCAPNG capture, reassemble IP
fragments, inspect packet payloads, and save edited capture data.

### Packet editing workflow

1. Select **File > Open Capture...** and choose a `.pcap` or `.pcapng` file.
2. Select a packet in **Reassembled packets**.
3. To decode payload fields, open **Packet Definition > Payload Struct
   Definitions...** and configure one or more matching definitions.
4. In the lower pane, edit the packet's hex data or a decoded field value.
5. Select **File > Save Capture** or **Save Capture As...**.

### Reassembled packets pane

The upper pane lists packet number, timestamp, IP version, source, destination,
protocol, identification, payload length, reassembly status, and payload bytes.

- Select a **Complete** packet to display and edit its payload in the lower
  pane. All columns in the upper pane are read-only.
- An **Incomplete** packet is read-only because all fragments are not available.
- When a packet contains multiple fragments, expand it to inspect each fragment.
  Fragment rows are read-only.

### Decoded packet data pane

The lower pane displays and edits the payload of the selected complete packet.
If no payload structure definition matches, the header displays **Payload: Hex
only**. Edit the **hex** column, entering exactly the number of bytes shown in
the row. Use **Bytes/row** to change how the payload bytes are grouped. All
other columns are read-only in this mode.

When a definition matches, the payload is decoded using the first matching
definition. Edit a field in the **value** column and press Enter or move focus
away to apply it. The payload is re-encoded, the capture bytes are updated, and
the packet is decoded again. The **hex** column and nested structure rows are
read-only, as are the other non-value columns.

### File and definition menus

- **Open Capture...** opens PCAP and PCAPNG files.
- **Save Capture** overwrites the current capture.
- **Save Capture As...** saves it to another PCAP or PCAPNG file.
- **Payload Struct Definitions...** opens the ordered payload matching rules.
- **Exit** closes the Packet Data Editor.

## Payload Struct Definition Editor Window

This window maps packet conditions to StructLayout definitions. Rules are
checked from top to bottom, and the first matching rule is used.

### Managing rules

- **Add** creates a rule with the condition `True`.
- **Remove** deletes the selected rule.
- **Move Up** and **Move Down** change matching priority.
- Select a row to edit its condition and root structure, then select **Update**
  to apply those values to the row.
- **Load StructLayout...** loads a JSON layout into the selected rule.

A condition can refer to `key`, `payload`, `ip_version`, `source`,
`destination`, `protocol`, and `identification`. Conditions must be valid
expressions supported by the layout expression evaluator. Enum values defined
in the layout's EnumDefDict can also be used in conditions.

The **Type Definition** menu selects the root structure or opens the StructDef
and EnumDef editors for the selected rule. The **File** menu opens and saves the
complete ordered rule list as JSON. Closing the window keeps the current rules
in the Packet Data Editor; use **Save** when the rules must also be stored in a
file.

## StructDef Dict Editor Window

This window edits the structures contained in the active StructLayout.

### Structures

- **Add Struct** and **Remove Struct** manage the structure list.
- Select a structure to edit its name and description.
- Select **Update Meta** to apply name or description changes.

### Fields

- **Add Field**, **Insert Field**, and **Remove Field** manage fields.
- **Shift Offset** moves the offsets of the selected fields by a byte and bit
  amount.
- **Update Multi-line Size** assigns a size to all selected fields.
- **Initial Size** and the adjacent type selector set defaults for new fields.
- Edit cells directly to change `name`, `offset`, `size`, `type`, `scale`,
  `repeat`, `description`, `range_expression`, `enum_def_name`, and
  `byte_swap`.

Offsets and sizes accept `byte,bit` values such as `1,3`. They may also use
layout expressions where supported. Select **Update** to apply all definitions
to the parent layout, or **Cancel** to discard changes made in this window.

## EnumDef Dict Editor Window

This window edits named integer values used by fields in the active
StructLayout.

- **Add Enum** and **Remove Enum** manage enum definitions.
- Edit the selected enum's name and description, then select **Update Meta**.
- **Add Value** appends a value using **Start Value** as the starting point.
- **Insert Value** inserts a value before the selected row.
- **Shift Value** adds or subtracts an amount from selected values.
- **Remove Value** deletes selected rows.
- Edit value names and integer values directly in the table.

Select **Update** to apply all enum definitions to the parent layout, or
**Cancel** to discard changes made in this window.
