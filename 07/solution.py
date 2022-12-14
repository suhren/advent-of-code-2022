import typing as t
from dataclasses import dataclass, field

@dataclass
class Entry:
    verb: str
    noun: t.Optional[str]
    output: t.Optional[t.List[str]]

@dataclass
class File:
    name: str
    size: int

@dataclass
class Directory:
    name: str
    size: int = None
    parent: "Directory" = None
    subdirs: t.Dict[str, "Directory"] = field(default_factory=dict)
    files: t.Dict[str, File] = field(default_factory=dict)

    def resolve_size(self):
        file_size = sum(file.size for file in self.files.values())
        subdir_size = sum(subdir.resolve_size() for subdir in self.subdirs.values())
        self.size = file_size + subdir_size
        return self.size

    def traverse(self):
        yield self
        for subdir in self.subdirs.values():
            yield from subdir.traverse()


entries = []

with open("input.txt", "r") as f:

    cmd_entries = [x.strip().split("\n") for x in f.read().split("$")[1:]]

    for lines in cmd_entries:
        cmd_parts = lines[0].split()
        verb = cmd_parts[0]
        noun = cmd_parts[1] if len(cmd_parts) > 1 else None
        output = lines[1:] if len(lines) > 1 else None
        entries.append(Entry(verb=verb, noun=noun, output=output))

root = Directory(name="/")
cwd = root

#print("\n".join(map(str, commands[:10])))

for entry in entries:
    match entry.verb:
        case "cd":
            match entry.noun:
                case "/":
                    cwd = root
                case "..":
                    cwd = cwd.parent
                case x:
                    if entry.noun in cwd.subdirs:
                        cwd = cwd.subdirs[x]
                    else:
                        cwd.subdirs[x] = Directory(name=x, parent=cwd)
                        cwd = cwd.subdirs[x]
        case "ls":
            for line in entry.output:
                if not line.startswith("dir"):
                    size_str, name = line.split()
                    cwd.files[name] = File(name=name, size=int(size_str))

root.resolve_size()


# Part 1

total_size = 0

for subdir in root.traverse():
    if subdir.size <= 100000:
        total_size += subdir.size

print(f"Sum of sizes of directories: {total_size}")


# Part 2

total_space = 70000000
used_space = root.size
free_space = total_space - used_space

required_space = 30000000
size_to_free = required_space - free_space

best_size = total_space

for subdir in root.traverse():
    if subdir.size < best_size and subdir.size >= size_to_free:
        best_size = subdir.size

print(f"Smallest found size of directory: {best_size}")
