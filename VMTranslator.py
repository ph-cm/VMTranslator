import sys

class Parser:
    def __init__(self, input_file):
        self.file = open(input_file, 'r')
        self.current_command = None

    def has_more_commands(self):
        self.current_command = self.file.readline()
        return bool(self.current_command)

    def advance(self):
        if self.has_more_commands():
            line = self.current_command.strip()
            if "//" in line:
                line = line.split("//")[0].strip()  # Remove comentários
            return line if line else None
        return None

    def close(self):
        self.file.close()


class CodeWriter:
    def __init__(self, output_file):
        self.file = open(output_file, 'w')
        self.label_count = 0

    def write_arithmetic(self, command):
        asm_code = ""
        if command == "add":
            asm_code = (
                "@SP\nAM=M-1\nD=M\n"  # Decrementa SP e armazena o valor no D
                "@SP\nAM=M-1\nM=D+M\n"  # Soma os dois valores no topo da pilha
                "@SP\nM=M+1\n"  # Incrementa SP
            )
        self.file.write(asm_code)

    def write_push_pop(self, command, segment, index):
        asm_code = ""
        if command == "push" and segment == "constant":
            asm_code = (
                f"@{index}\nD=A\n"  # D = constante
                "@SP\nA=M\nM=D\n"  # *SP = constante
                "@SP\nM=M+1\n"  # SP++
            )
        self.file.write(asm_code)

    def close(self):
        self.file.close()


def main():
    if len(sys.argv) != 2:
        print("Uso: python VMTranslator.py simpleadd.vm")
        return

    input_file = sys.argv[1]
    output_file = input_file.replace(".vm", ".asm")

    parser = Parser(input_file)
    code_writer = CodeWriter(output_file)

    while True:
        command = parser.advance()
        if command is None:
            break
        tokens = command.split()
        cmd_type = tokens[0]

        if cmd_type == "push":
            code_writer.write_push_pop(cmd_type, tokens[1], tokens[2])
        elif cmd_type == "add":
            code_writer.write_arithmetic(cmd_type)

    parser.close()
    code_writer.close()
    print(f"Tradução concluída: {output_file}")


if __name__ == "__main__":
    main()

#parse
#Lê o arquivo .vm linha por linha e remove comentários

#CodeWriter
#write_arithmetic: Escreve o código de assembly para comandos aritméticos (add).
#write_push_pop: Implementa o comando push constant X.
#Escreve o código Hack em output_file

#main
#Processa o arquivo .vm passado como argumento.
#Usa o Parser para ler cada comando e o CodeWriter para gerar o código Hack equivalente.