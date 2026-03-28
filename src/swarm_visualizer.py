import sys
import numpy as np
from vispy import scene, app
from nexus_force_core_gravity import NGigaForgePhysics

class SwarmCanvas(scene.SceneCanvas):
    """
    Visualizador OpenGL Ligero para N-Giga-Forge Swarm.
    Muestra los primeros 50k agentes para monitoreo en tiempo real.
    """
    def __init__(self, physics_engine):
        scene.SceneCanvas.__init__(self, keys='interactive', show=True, 
                                 title='N-GIGA-FORGE VISUALIZER v1.0',
                                 bgcolor='black')
        self.unfreeze()
        self.physics = physics_engine
        
        # Configuración de Viewport
        self.view = self.central_widget.add_view()
        self.view.camera = 'turntable'
        self.view.camera.distance = 5.0
        
        # El Enjambre Pasivo (Primeros 50,000)
        self.scatter = scene.visuals.Markers()
        self.view.add(self.scatter)
        
        # La Sonda (Agente [0])
        self.probe_marker = scene.visuals.Markers()
        self.view.add(self.probe_marker)
        
        # Estrella Central (Origen)
        self.star = scene.visuals.Markers()
        self.view.add(self.star)
        self.star.set_data(np.array([[0, 0, 0]]), edge_color=None, face_color='yellow', size=15)

        self.timer = app.Timer('auto', connect=self.on_timer, start=True)
        self.freeze()

    def on_timer(self, event):
        # 1. Ejecutar un paso de física en el motor
        self.physics.update_passive_swarm()
        self.physics.update_probe()
        
        # 2. Extraer datos para render (Puntos)
        data = self.physics.get_render_data()
        
        # 3. Actualizar Visuales
        # Swarm (Blanco, Dim 2)
        self.scatter.set_data(data[1:], edge_color=None, face_color=(1, 1, 1, 0.5), size=2)
        
        # Sonda (Rojo, Dim 10)
        self.probe_marker.set_data(data[0:1], edge_color=None, face_color='red', size=10)
        
        self.update()

if __name__ == "__main__":
    # Inicializar motor físico
    engine = NGigaForgePhysics(agent_count=50000) # Reducción para visualización fluida
    canvas = SwarmCanvas(engine)
    
    if sys.flags.interactive != 1:
        app.run()
