class Entry:

    def __init__(self, title, num_order, comments, points):
        self.title = title
        self.num_order = num_order
        self.comments = comments
        self.points = points
        self.title_length = len(title.split())

    def __str__(self):
        return 'Title: ' + self.title + '\nNumber of the order: ' + str(self.num_order) + '\nComments: ' + str(self.comments) + '\nPoints: ' + str(self.points)
