from flask import Flask, render_template, request
import sys

app = Flask(__name__)

class Process:
    def __init__(self, name, arrival_time, burst_time):
        self.name = name
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.completion_time = 0
        self.turnaround_time = 0
        self.waiting_time = 0

def sjf_scheduling(processes):
    processes.sort(key=lambda x: x.arrival_time)
    current_time = 0
    completed = 0
    n = len(processes)
    is_completed = [False] * n

    while completed < n:
        idx = -1
        min_burst = sys.maxsize

        for i in range(n):
            if processes[i].arrival_time <= current_time and not is_completed[i]:
                if processes[i].burst_time < min_burst:
                    min_burst = processes[i].burst_time
                    idx = i
                elif processes[i].burst_time == min_burst:
                    if processes[i].arrival_time < processes[idx].arrival_time:
                        idx = i

        if idx != -1:
            current_time += processes[idx].burst_time
            processes[idx].completion_time = current_time
            processes[idx].turnaround_time = processes[idx].completion_time - processes[idx].arrival_time
            processes[idx].waiting_time = processes[idx].turnaround_time - processes[idx].burst_time
            is_completed[idx] = True
            completed += 1
        else:
            current_time += 1

    return processes

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        n = int(request.form['n'])
        processes = []

        for i in range(n):
            name = request.form[f'name_{i}']
            arrival_time = int(request.form[f'arrival_time_{i}'])
            burst_time = int(request.form[f'burst_time_{i}'])
            processes.append(Process(name, arrival_time, burst_time))

        processes = sjf_scheduling(processes)

        total_waiting_time = sum(p.waiting_time for p in processes)
        total_turnaround_time = sum(p.turnaround_time for p in processes)
        average_waiting_time = total_waiting_time / n if n > 0 else 0
        average_turnaround_time = total_turnaround_time / n if n > 0 else 0

        return render_template(
            'result.html',
            processes=processes,
            average_waiting_time=average_waiting_time,
            average_turnaround_time=average_turnaround_time
        )

    return render_template('input.html')

if __name__ == '__main__':
    app.run(debug=True)
