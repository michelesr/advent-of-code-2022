def up(start_x: int, start_y: int, end_x: int, end_y: int) -> list[tuple[int, int]]:
    return [(start_x, n) for n in range(start_y, end_y - 1, -1)]


def down(start_x: int, start_y: int, end_x: int, end_y: int) -> list[tuple[int, int]]:
    return [(start_x, n) for n in range(start_y, end_y + 1, 1)]


def left(start_x: int, start_y: int, end_x: int, end_y: int) -> list[tuple[int, int]]:
    return [(n, start_y) for n in range(start_x, end_x - 1, -1)]


def right(start_x: int, start_y: int, end_x: int, end_y: int) -> list[tuple[int, int]]:
    return [(n, start_y) for n in range(start_x, end_x + 1, 1)]


def get_points(
    start_x: int, start_y: int, end_x: int, end_y: int
) -> list[tuple[int, int]]:
    if start_y == end_y:
        if start_x < end_x:
            return right(start_x, start_y, end_x, end_y)
        elif start_x > end_x:
            return left(start_x, start_y, end_x, end_y)
    elif start_x == end_x:
        if start_y < end_y:
            return down(start_x, start_y, end_x, end_y)
        elif start_y > end_y:
            return up(start_x, start_y, end_x, end_y)
    raise ValueError(f"invalid range: {(start_x, start_y)} -> {(end_x, end_y)}")


def go(max_depth: int, rocks: list[tuple[int, int]], part_two: bool = False) -> int:
    steps = 0
    while True:
        # rock starts
        a, b = (500, 0)

        end = False
        res = None
        while True:
            if (not part_two and b > max_depth) or (part_two and (500, 0) in rocks):
                end = True
                break

            if part_two and b > max_depth:
                res = a, b
                break

            # down?
            if (a, b + 1) not in rocks:
                b += 1
                continue

            # left?
            elif (a - 1, b + 1) not in rocks:
                a, b = a - 1, b + 1

            # right?
            elif (a + 1, b + 1) not in rocks:
                a, b = a + 1, b + 1

            else:
                res = a, b
                break

        if end:
            break

        if not res:
            raise Exception("res not set")

        rocks.append(res)
        if not part_two:
            # in part two max_depth is static
            max_depth = max(max_depth, res[1])
        steps += 1
    return steps


with open("input", "r") as file:
    lines: list[list[str]] = [
        line.strip("\n").replace(" ", "").split("->") for line in file.readlines()
    ]

paths: list[list[tuple[str, str]]] = []
for i in range(len(lines)):
    paths.append([tuple(element.split(",")) for element in lines[i]])

rocks: list[tuple[int, int]] = []
for path in paths:
    for i in range(len(path) - 1):
        a, b = path[i]
        x, y = path[i + 1]
        a, b = int(a), int(b)
        x, y = int(x), int(y)
        rocks += get_points(x, y, a, b)


# part one
max_depth = max((r[1] for r in rocks))
print(go(max_depth, rocks.copy()))

# part two
print(go(max_depth, rocks.copy(), part_two=True))
