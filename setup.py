from setuptools import find_packages, setup

package_name = 'localization'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
        ['resource/localization']),
    ('share/localization', ['package.xml']),

    ('share/localization/config', ['config/ekf.yaml']),
    ('share/localization/launch', ['launch/ekf.launch.py']),

    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='asmaa',
    maintainer_email='you@example.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    }, # Camera Visual Odometry (placeholder)
    
    entry_points={
        'console_scripts': [
            'localization = localization.localization:main'
        ],
    },
)
