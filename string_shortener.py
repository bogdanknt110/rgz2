def short_line(initial_line, offset=0):
    current_len = len(initial_line)
    removed_len = current_len - final_len
    return (
        initial_line[ : current_len // 2 - removed_len // 2 + offset],
        initial_line[current_len // 2 - removed_len // 2 + removed_len + offset : ],
    )

def count_initial(short, i):
    short = short[0]
    k = i + 1
    while k < line_count and (initial_lines[k].startswith(short) or initial_lines[k] == ''):
        k += 1
    a = k
    k = i - 1
    while k >= 0  and (initial_lines[k].startswith(short) or initial_lines[k] == ''):
        k -= 1
    b = k + 1
    return (b, a)

def count_reversed(short, j):
    short = short[1]
    k = j + 1
    while k < line_count and (reversed_lines[k].endswith(short) or reversed_lines[k] == ''):
        k += 1
    a = k
    k = j - 1
    while k >= 0  and (reversed_lines[k].endswith(short) or reversed_lines[k] == ''):
        k -= 1
    b = k + 1
    return (b, a)

line_count = int(input())

lines = []

initial_lines = []
reversed_lines = []

for i in range(line_count):
    lines.append(input())
    initial_lines.append((lines[i], i))
    reversed_lines.append((lines[i][::-1], i))

initial_lines.sort()
reversed_lines.sort()

initial_ind = {}
reversed_ind = {}

back_initial_ind = {}
back_reversed_ind = {}

for i in range(line_count):
    initial_ind[initial_lines[i][1]] = i
    reversed_ind[reversed_lines[i][1]] = i
    back_initial_ind[i] = initial_lines[i][1]
    back_reversed_ind[i] = reversed_lines[i][1]
    initial_lines[i] = initial_lines[i][0]
    reversed_lines[i] = reversed_lines[i][0][::-1]

final_len = int(input())

flag = True
while flag:
    flag = False
    unresolved_lines = {}
    for ind in range(len(lines)):
        if type(lines[ind]) != type(''):
            continue
        short = short_line(lines[ind])
        i = initial_ind[ind]
        j = reversed_ind[ind]
        if (count_initial(short, i) != (i, i + 1) and count_reversed(short, j) != (j, j + 1)) or short in lines:
            if not(short in lines):
                a = count_initial(short, i)
                b = count_reversed(short, j)
                counts = {0 : min(a[1] - a[0] - 1, b[1] - b[0] - 1)}
            min_offset = len(short[0])
            max_offset = len(short[1])
            for k in range(1, max_offset):
                short = short_line(lines[ind], k)
                if short in lines:
                    continue
                counts[k] = count_initial(short, i)
                counts[k] = counts[k][1] - counts[k][0] - 1
            for k in range(1, min_offset):
                short = short_line(lines[ind], -k)
                if short in lines:
                    continue
                counts[-k] = count_reversed(short, j)
                counts[-k] = counts[-k][1] - counts[-k][0] - 1
            minsim = min(counts.values())
            offsets = [key for key, value in counts.items() if value == minsim]
            if (minsim == 0):
                initial_lines[i] = ''
                reversed_lines[j] = ''
                short = short_line(lines[ind], offsets[0])
                lines[ind] = short
                flag = True
                continue
            minsim = line_count * [0]
            offset_with_min_sim = 0
            for k in offsets:
                short = short_line(lines[ind], k)
                if k < 0:
                    cnt = count_reversed(short, j)
                    sim = [back_reversed_ind[x] for x in range(cnt[0], cnt[1]) if initial_lines[initial_ind[back_reversed_ind[x]]].startswith(short[0])]
                if k > 0:
                    cnt = count_initial(short, i)
                    sim = [back_initial_ind[x] for x in range(cnt[0], cnt[1]) if reversed_lines[reversed_ind[back_initial_ind[x]]].endswith(short[1])]
                if k == 0:
                    cnt_initial = count_initial(short, i)
                    cnt_reversed = count_reversed(short, j)
                    if (cnt_initial[1] - cnt_initial[0] < cnt_reversed[1] - cnt_reversed[0]):
                        sim = [back_initial_ind[x] for x in range(cnt_initial[0], cnt_initial[1]) if reversed_lines[reversed_ind[back_initial_ind[x]]].endswith(short[1])]
                    else:
                        sim = [back_reversed_ind[x] for x in range(cnt_reversed[0], cnt_reversed[1]) if initial_lines[initial_ind[back_reversed_ind[x]]].startswith(short[0])]
                sim.remove(ind)
                if len(sim) < len(minsim):
                    minsim = sim
                    offset_with_min_sim = k
                if len(minsim) == 0:
                    break
            if len(minsim) == 0:
                short = short_line(lines[ind], offset_with_min_sim)
                initial_lines[i] = ''
                reversed_lines[j] = ''
                lines[ind] = short
                flag = True
                continue
            unresolved_lines[ind] = (offset_with_min_sim, minsim)
        else:
            initial_lines[i] = ''
            reversed_lines[j] = ''
            lines[ind] = short
            flag = True

dups = {}

for ind in unresolved_lines:
    short = short_line(lines[ind], unresolved_lines[ind][0])
    if short in lines:
        best_short = short
        for k in range(-len(best_short[0]) + 1, len(best_short[1])):
            short = short_line(lines[ind], k)
            if not(short in lines):
                lines[ind] = short
                break
        if type(lines[ind]) == type(''):
            lines[ind] = best_short
            if best_short in dups:
                dups[best_short] += 1
            else:
                dups[best_short] = 0
    else:
        lines[ind] = short

flag = False

for dup in dups:
    if dups[dup] > 9:
        flag = True
        break

if flag:
    print('CAN NOT SHORT ALL LINES')
    exit(0)

used_dups = {}

for line in lines:
    if line in dups:
        if line in used_dups:
            print(line[0] + '…' + line[1] + '_' + str(used_dups[line]))
            used_dups[line] += 1
        else:
            print(line[0] + '…' + line[1])
            used_dups[line] = 0
    else:
        print(line[0] + '…' + line[1])
