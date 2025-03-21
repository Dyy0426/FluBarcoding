import os
import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import filedialog
from tqdm import tqdm
from openpyxl import Workbook
from openpyxl.styles import Font
import random


# 获取文件夹路径并读取xlsx文件
def get_xlsx_files():
    root = tk.Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory()
    xlsx_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.xlsx')]
    return xlsx_files


# 更复杂的蒙特卡罗模拟计算函数
def monte_carlo_simulation(sequence, temperature):
    # 状态生成：假设每个氨基酸有三种构象
    conformations = [random.choice(['A', 'B', 'C']) for _ in sequence]

    # 能量计算：简单的模型，假设每个构象有不同的能量
    energies = {'A': -1.0, 'B': -0.5, 'C': 0.0}
    total_energy = sum(energies[conf] for conf in conformations)

    # 马尔科夫链蒙特卡罗模拟
    def metropolis_criteria(delta_energy, temperature):
        if delta_energy < 0:
            return True
        else:
            return np.exp(-delta_energy / (0.001987 * (temperature + 273.15))) > random.random()

    for _ in range(1000):
        i = random.randint(0, len(sequence) - 1)
        new_conf = random.choice(['A', 'B', 'C'])
        delta_energy = energies[new_conf] - energies[conformations[i]]

        if metropolis_criteria(delta_energy, temperature):
            conformations[i] = new_conf
            total_energy += delta_energy

    # 参数计算：基于选定的构象计算热力学参数
    Tm = 70 + random.uniform(-5, 5)  # 模拟熔解温度
    ΔG = total_energy  # 自由能变化
    ΔH = total_energy * 2  # 焓变
    ΔS = total_energy * 3  # 熵变
    ΔCp = total_energy * 0.1  # 热容变化
    Kd = np.exp(-ΔG / (0.001987 * (temperature + 273.15)))  # 结合常数
    return Tm, ΔG, ΔH, ΔS, ΔCp, Kd


# 计算热力学参数
def calculate_thermodynamic_parameters(sequence):
    temperatures = [4, 20, 25, 37, 42, 55, 72, 95]
    results = []

    for temp in temperatures:
        Tm, ΔG, ΔH, ΔS, ΔCp, Kd = monte_carlo_simulation(sequence, temp)
        results.append([temp, Tm, ΔG, ΔH, ΔS, ΔCp, Kd])

    return results


# 导入xlsx文件并处理
def process_files(files):
    for file in files:
        df = pd.read_excel(file)
        sequences = df.iloc[:, 0].astype(str).tolist()

        all_results = []

        # 显示进度条
        for seq in tqdm(sequences, desc=f'Processing {os.path.basename(file)}'):
            results = calculate_thermodynamic_parameters(seq)
            # 将结果进行合并处理
            temp_results = [seq]
            if results:
                temp_results += [results[0][1], results[0][3], results[0][4], results[0][5],
                                 results[0][6]]  # Tm, ΔH, ΔS, ΔCp, Kd
                temp_results += [r[2] for r in results]  # 所有温度下的ΔG

            all_results.append(temp_results)

        # 创建一个新的DataFrame用于结果存储
        columns = ["Sequence", "Tm (°C)", "ΔH (kcal/mol)", "ΔS (cal/(mol*K))", "ΔCp (kcal/(mol*K))", "Kd (M)"]
        columns += [f"ΔG @ {temp}°C" for temp in [4, 20, 25, 37, 42, 55, 72, 95]]
        results_df = pd.DataFrame(all_results, columns=columns)

        # 计算平均值和标准差
        avg_row = ["Avg"] + results_df.iloc[:, 1:].mean().tolist()
        sd_row = ["SD"] + results_df.iloc[:, 1:].std().tolist()

        # 将结果和统计量写入到新的DataFrame
        results_df.loc[len(results_df)] = avg_row
        results_df.loc[len(results_df)] = sd_row

        # 创建一个新的工作簿并写入数据
        wb = Workbook()
        ws = wb.active
        ws.title = "Thermodynamic Parameters"

        # 写入表头
        ws.append(columns)
        for cell in ws[1]:
            cell.font = Font(bold=True)

        # 写入数据
        for row in results_df.itertuples(index=False):
            ws.append(row)

        # 导出到新的xlsx文件
        output_file = f'aaSTR_data_Thfeatures-{os.path.splitext(os.path.basename(file))[0]}.xlsx'
        wb.save(output_file)


if __name__ == '__main__':
    xlsx_files = get_xlsx_files()
    process_files(xlsx_files)
