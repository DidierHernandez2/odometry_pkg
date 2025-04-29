from setuptools import find_packages, setup

package_name = 'odometry_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='darhf',
    maintainer_email='didier.hernandez1972@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
<<<<<<< HEAD
            'dead_reckoning = odometry_pkg.dead_reckoning:main',
=======
            'dead_reckoning = odometry_pkg.dead_reckoning:main'
>>>>>>> d34c3ea (Cambio de paquete)
        ],
    },
)
