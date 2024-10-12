Welcome to MasterPiece documentation!
=====================================

.. image:: _static/masterpiece.png
    :alt: Masterpiece - A Piece of Work
    :width: 400px
    :height: 300px

.. toctree::
   :maxdepth: 2
   :caption: Contents:


   README
   CHANGELOG
   LICENSE
   CONTRIBUTING
   TODO
   masterpiece/index




Classes
-------

.. inheritance-diagram:: masterpiece.base.MasterPiece masterpiece.base.Composite masterpiece.base.Application masterpiece.base masterpiece.base.Plugin masterpiece.base.PlugMaster
   :parts: 1



Instances
---------

Instances of these classes can be grouped into hierarchical structure to model real world apparatuses.


Instance Diagram
----------------

.. mermaid::

   classDiagram
       class MainCompositeObject {
           MasterPiece1: MasterPiece
           SubCompositeObject: SubCompositeObject
       }
       class SubCompositeObject {
           SubMasterPiece1: MasterPiece
           SubMasterPiece2: MasterPiece
       }
       MainCompositeObject --> MasterPiece1 : contains
       MainCompositeObject --> SubCompositeObject : contains
       SubCompositeObject --> SubMasterPiece1 : contains
       SubCompositeObject --> SubMasterPiece2 : contains


Index
=====

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
