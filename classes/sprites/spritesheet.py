import pygame


class SpriteSheet:
    def __init__(
        self,
        rows: int,
        columns: int,
        image: str | pygame.Surface,
        frame_width: int,
        frame_heigth: int,
        x_offset: int = 0,
        y_offset: int = 0,
        scale_by: float = 1
    ):
        self.rows = rows
        self.columns = columns

        if isinstance(image, str):
            self.image = pygame.image.load(image)
        else:
            self.image = image
        self.frame_width = frame_width
        self.frame_heigth = frame_heigth
        self.frame_offset = [x_offset, y_offset]
        self.scale_factor = scale_by

        self.frames = self.load_frames()

        for i, row in enumerate(self.frames):
            for j, frame in enumerate(row):
                self.frames[i][j] = pygame.transform.scale_by(frame, self.scale_factor)
    
    def load_frames(self):
        frames = []
        for row in range(self.rows):
            direction_frames = []
            for col in range(self.columns):
                x = col * self.frame_width + (col+1)*self.frame_offset[0]
                y = row * self.frame_heigth + (row+1)*self.frame_offset[1]
                frame = self.image.subsurface(pygame.Rect(x, y, self.frame_width, self.frame_heigth))
                
                # Escala o quadro para 2.5x o tamanho original
                scaled_frame = pygame.transform.scale(
                    frame, (int(self.frame_width), int(self.frame_heigth))
                )
                
                direction_frames.append(scaled_frame)  # Adiciona o quadro escalado à direção atual
            frames.append(direction_frames)  # Adiciona os quadros da direção à lista principal
        return frames

    def __len__(self):
        return len(self.frames)

    def __getitem__(self, item):
        return self.frames[item]
