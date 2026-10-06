import matplotlib.pyplot as plt
import numpy as np

def plot_8085_cycle(title, filename, num_tstates=3, is_write=False):
    fig, ax = plt.subplots(figsize=(8, 5))
    
    t = np.linspace(0, num_tstates, 500)
    
    # Clock Signal
    clk = np.sin(2 * np.pi * t * 1) > 0
    ax.plot(t, clk + 12, 'b', label='CLK')
    
    # ALE Signal
    ale = np.where(t < 0.8, 1, 0)
    ax.plot(t, ale + 10, 'g', label='ALE')
    
    # Address Bus A15-A8
    ax.fill_between(t, 8, 9, color='lightgray', alpha=0.5)
    ax.text(num_tstates/2, 8.4, 'High Address / Port', ha='center', va='center')
    
    # Multiplexed Address/Data Bus AD7-AD0
    ax.plot([0, 0.8, 1.0, num_tstates], [6.5, 6.5, 6.5, 6.5], 'k--')
    ax.text(0.4, 6.5, 'Low Address', ha='center', va='center', bbox=dict(boxstyle="round", fc="white"))
    ax.text((num_tstates+1)/2, 6.5, 'Data Out' if is_write else 'Data In', ha='center', va='center', bbox=dict(boxstyle="round", fc="white"))
    
    # Read/Write Control Signals
    rd = np.where((t >= 1.2) & (t <= num_tstates - 0.2) & (not is_write), 0, 1)
    wr = np.where((t >= 1.2) & (t <= num_tstates - 0.2) & is_write, 0, 1)
    
    ax.plot(t, rd + 4, 'r', label="RD'")
    ax.plot(t, wr + 2, 'm', label="WR'")
    
    ax.set_yticks([12.5, 10.5, 8.5, 6.5, 4.5, 2.5])
    ax.set_yticklabels(['CLK', 'ALE', 'A15-A8', 'AD7-AD0', "RD'", "WR'"])
    ax.set_xticks(np.arange(0.5, num_tstates, 1))
    ax.set_xticklabels([f'T{i+1}' for i in range(num_tstates)])
    
    plt.title(f'8085 Timing Diagram: {title}')
    plt.grid(True, axis='x', linestyle='--')
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.close()

# Generate all 5 primary machine cycle PNG diagrams
plot_8085_cycle("Opcode Fetch Machine Cycle", "1_opcode_fetch.png", num_tstates=4, is_write=False)
plot_8085_cycle("Memory Read Machine Cycle", "2_memory_read.png", num_tstates=3, is_write=False)
plot_8085_cycle("Memory Write Machine Cycle", "3_memory_write.png", num_tstates=3, is_write=True)
plot_8085_cycle("I/O Read Machine Cycle", "4_io_read.png", num_tstates=3, is_write=False)
plot_8085_cycle("I/O Write Machine Cycle", "5_io_write.png", num_tstates=3, is_write=True)

print("Success! All 5 timing diagram image files (.png) have been saved.")