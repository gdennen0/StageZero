class LocalController:
    def __init__(self, local_window, main_controller):
        self.nodes = None
        self.node_total = None
        self.start_data = None
        self.end_data = None
        self.sequence_outputs = None

    def run_sequence(self, nodes, start_data):
        x = start_data
        sequence_outputs = []

        count = 0
        for node in nodes.items():
            x = node.transform(x)
            self.sequence_outputs.append(x)
            print(f"Node {count} value is {x}")
            count = count + 1

    def preview_transform_sequence(self, sequence_outputs):
        self.loaded_plot = None
        self.local_view.open_preview()
        self.initialize_connections()

    def initialize_connections(self):
        self.local_view.next_button.clicked.connect(self.on_next_click)
        self.local_view.prev_button.clicked.connect(self.on_prev_click)

    def load_plot(self, index):
        plot_data = self.nodes[index]
        self.plot.clear()
        self.plot.plot(plot_data)

    def on_next_click(self):
        if self.loaded_plot_index is not self.node_total:
            self.loaded_plot_index = self.loaded_plot_index + 1
            self.load_plot(self.loaded_plot_index)
        else:
            print(f"already on the last plot")

    def on_prev_click(self):
        if self.loaded_plot_index is not 0:
            self.loaded_plot_index = self.loaded_plot_index - 1
            self.load_plot(self.loaded_plot_index)
        else:
            print(f"already on the first plot")
