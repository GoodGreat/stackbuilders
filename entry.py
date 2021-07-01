class Entry:

    def __init__(self, title, num_order, comments, points, title_length):
        self.title = title
        self.num_order = num_order
        self.comments = comments
        self.points = points
        self.title_length = len(title.split())
