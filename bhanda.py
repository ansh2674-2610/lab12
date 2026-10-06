import matplotlib.pyplot as plt
import numpy as np

def plot_instruction(title, filename, machine_cycles):
    """
    Generates full multi-cycle timing diagram for 8085 instructions.
    """
    total_t = sum(mc['t_states'] for mc in machine_cycles)
    fig, ax = plt.subplots(figsize=(max(12, total_t * 0.85), 6))
    
    t = np.linspace(0, total_t, total_t * 100)
    
    # 1. Clock Signal (CLK)
    clk = np.sin(2 * np.pi * t * 1) > 0
    ax.plot(t, clk + 14, 'b', linewidth=1)
    
    # 2. Address Latch Enable (ALE)
    ale = np.zeros_like(t)
    curr_t = 0
    for mc in machine_cycles:
        mask = (t >= curr_t) & (t < curr_t + 0.7)
        ale[mask] = 1
        curr_t += mc['t_states']
    ax.plot(t, ale + 11.5, 'g', linewidth=1.5)
    
    # 3. High Address Bus (A15-A8)
    ax.fill_between(t, 9.5, 10.5, color='lightgray', alpha=0.5)
    
    # 4. Multiplexed Bus Line (AD7-AD0)
    ax.plot([0, total_t], [8, 8], 'k--', alpha=0.3)
    
    # Control signals initialization
    rd = np.ones_like(t)
    wr = np.ones_like(t)
    iom = np.zeros_like(t)  # IO/M' = 0 for memory operations
    
    curr_t = 0
    for i, mc in enumerate(machine_cycles):
        t_start = curr_t
        t_end = curr_t + mc['t_states']
        
        # Address Bus Labels
        ax.text(t_start + mc['t_states']/2, 10, f"{mc['name']}\nAddr High", ha='center', va='center', fontsize=8)
        
        # AD7-AD0 Data Labels
        ax.text(t_start + 0.4, 8, 'Low Addr', ha='center', va='center', 
                bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="black", lw=0.5), fontsize=8)
        ax.text(t_start + (mc['t_states'] + 0.8)/2, 8, mc['label'], ha='center', va='center', 
                bbox=dict(boxstyle="round,pad=0.2", fc="#ffff99" if mc['type']=='write' else "#b3e0ff", ec="black", lw=0.5), fontsize=8)
        
        # RD' and WR' pulse active regions
        ctrl_start = t_start + 1.1
        ctrl_end = t_end - 0.2
        ctrl_mask = (t >= ctrl_start) & (t <= ctrl_end)
        
        if mc['type'] == 'read':
            rd[ctrl_mask] = 0
        elif mc['type'] == 'write':
            wr[ctrl_mask] = 0
            
        # Draw dotted vertical separators between machine cycles
        if i > 0:
            ax.axvline(x=t_start, color='red', linestyle=':', alpha=0.6)
            
        curr_t = t_end

    # Plot Control Signals
    ax.plot(t, iom + 5.5, 'c', linewidth=1.5)
    ax.plot(t, rd + 3, 'r', linewidth=1.5)
    ax.plot(t, wr + 0.5, 'm', linewidth=1.5)
    
    # Y-Axis Formatting
    ax.set_yticks([14.5, 12, 10, 8, 5.5, 3.5, 1])
    ax.set_yticklabels(['CLK', 'ALE', 'A15-A8', 'AD7-AD0', "IO/M'", "RD'", "WR'"])
    
    # X-Axis Formatting
    ax.set_xticks(np.arange(0.5, total_t, 1))
    ax.set_xticklabels([f'T{i+1}' for i in range(total_t)], fontsize=8)
    
    plt.title(f'8085 Instruction Timing Diagram: {title} ({total_t} T-States)', fontsize=12, fontweight='bold')
    plt.grid(True, axis='x', linestyle='--', alpha=0.4)
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.close()
    print(f"Generated and saved: {filename}")

# --- Instruction Definitions ---

# f. LDA addr (4 Machine Cycles, 13 T-States)
lda_cycles = [
    {'name': 'MC1 (OF)', 't_states': 4, 'type': 'read', 'label': 'LDA Opcode'},
    {'name': 'MC2 (MR)', 't_states': 3, 'type': 'read', 'label': 'Addr LSB'},
    {'name': 'MC3 (MR)', 't_states': 3, 'type': 'read', 'label': 'Addr MSB'},
    {'name': 'MC4 (MR)', 't_states': 3, 'type': 'read', 'label': 'Data -> Acc'}
]

# f. STA addr (4 Machine Cycles, 13 T-States)
sta_cycles = [
    {'name': 'MC1 (OF)', 't_states': 4, 'type': 'read', 'label': 'STA Opcode'},
    {'name': 'MC2 (MR)', 't_states': 3, 'type': 'read', 'label': 'Addr LSB'},
    {'name': 'MC3 (MR)', 't_states': 3, 'type': 'read', 'label': 'Addr MSB'},
    {'name': 'MC4 (MW)', 't_states': 3, 'type': 'write', 'label': 'Acc -> Mem'}
]

# g. LHLD addr (5 Machine Cycles, 16 T-States)
lhld_cycles = [
    {'name': 'MC1 (OF)', 't_states': 4, 'type': 'read', 'label': 'LHLD Opcode'},
    {'name': 'MC2 (MR)', 't_states': 3, 'type': 'read', 'label': 'Addr LSB'},
    {'name': 'MC3 (MR)', 't_states': 3, 'type': 'read', 'label': 'Addr MSB'},
    {'name': 'MC4 (MR)', 't_states': 3, 'type': 'read', 'label': 'Mem -> L'},
    {'name': 'MC5 (MR)', 't_states': 3, 'type': 'read', 'label': 'Mem+1 -> H'}
]

# g. SHLD addr (5 Machine Cycles, 16 T-States)
shld_cycles = [
    {'name': 'MC1 (OF)', 't_states': 4, 'type': 'read', 'label': 'SHLD Opcode'},
    {'name': 'MC2 (MR)', 't_states': 3, 'type': 'read', 'label': 'Addr LSB'},
    {'name': 'MC3 (MR)', 't_states': 3, 'type': 'read', 'label': 'Addr MSB'},
    {'name': 'MC4 (MW)', 't_states': 3, 'type': 'write', 'label': 'L -> Mem'},
    {'name': 'MC5 (MW)', 't_states': 3, 'type': 'write', 'label': 'H -> Mem+1'}
]

# Execute plot generator
plot_instruction('LDA addr', 'lda_instruction.png', lda_cycles)
plot_instruction('STA addr', 'sta_instruction.png', sta_cycles)
plot_instruction('LHLD addr', 'lhld_instruction.png', lhld_cycles)
plot_instruction('SHLD addr', 'shld_instruction.png', shld_cycles)