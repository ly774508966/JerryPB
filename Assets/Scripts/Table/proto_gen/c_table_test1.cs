//------------------------------------------------------------------------------
// <auto-generated>
//     This code was generated by a tool.
//
//     Changes to this file may cause incorrect behavior and will be lost if
//     the code is regenerated.
// </auto-generated>
//------------------------------------------------------------------------------

// Option: missing-value detection (*Specified/ShouldSerialize*/Reset*) enabled
    
// Generated from: c_table_test1.proto
// Note: requires additional types generated from: common_effect.proto
// Note: requires additional types generated from: common_degree.proto
namespace Table
{
  [global::System.Serializable, global::ProtoBuf.ProtoContract(Name=@"test1")]
  public partial class test1 : global::ProtoBuf.IExtensible
  {
    public test1() {}
    

    private int? _id;
    [global::ProtoBuf.ProtoMember(1, IsRequired = false, Name=@"id", DataFormat = global::ProtoBuf.DataFormat.ZigZag)]
    public int id
    {
      get { return _id?? default(int); }
      set { _id = value; }
    }
    //Here has been replaced by XXMMLLDeleter
    [global::System.ComponentModel.Browsable(false)]
    public bool idSpecified
    {
      get { return _id != null; }
      set { if (value == (_id== null)) _id = value ? id : (int?)null; }
    }
    private bool ShouldSerializeid() { return idSpecified; }
    private void Resetid() { idSpecified = false; }
    

    private Common.Effect _name = null;
    [global::ProtoBuf.ProtoMember(2, IsRequired = false, Name=@"name", DataFormat = global::ProtoBuf.DataFormat.Default)]
    [global::System.ComponentModel.DefaultValue(null)]
    public Common.Effect name
    {
      get { return _name; }
      set { _name = value; }
    }

    private Common.DegreeQualityType? _degree_quality_type;
    [global::ProtoBuf.ProtoMember(3, IsRequired = false, Name=@"degree_quality_type", DataFormat = global::ProtoBuf.DataFormat.TwosComplement)]
    public Common.DegreeQualityType degree_quality_type
    {
      get { return _degree_quality_type?? Common.DegreeQualityType.DEGREE_INVALID; }
      set { _degree_quality_type = value; }
    }
    //Here has been replaced by XXMMLLDeleter
    [global::System.ComponentModel.Browsable(false)]
    public bool degree_quality_typeSpecified
    {
      get { return _degree_quality_type != null; }
      set { if (value == (_degree_quality_type== null)) _degree_quality_type = value ? degree_quality_type : (Common.DegreeQualityType?)null; }
    }
    private bool ShouldSerializedegree_quality_type() { return degree_quality_typeSpecified; }
    private void Resetdegree_quality_type() { degree_quality_typeSpecified = false; }
    
    private global::ProtoBuf.IExtension extensionObject;
    global::ProtoBuf.IExtension global::ProtoBuf.IExtensible.GetExtensionObject(bool createIfMissing)
      { return global::ProtoBuf.Extensible.GetExtensionObject(ref extensionObject, createIfMissing); }
  }
  
  [global::System.Serializable, global::ProtoBuf.ProtoContract(Name=@"test1_ARRAY")]
  public partial class test1_ARRAY : global::ProtoBuf.IExtensible
  {
    public test1_ARRAY() {}
    
    private readonly global::System.Collections.Generic.List<Table.test1> _rows = new global::System.Collections.Generic.List<Table.test1>();
    [global::ProtoBuf.ProtoMember(1, Name=@"rows", DataFormat = global::ProtoBuf.DataFormat.Default)]
    public global::System.Collections.Generic.List<Table.test1> rows
    {
      get { return _rows; }
    }
  
    private global::ProtoBuf.IExtension extensionObject;
    global::ProtoBuf.IExtension global::ProtoBuf.IExtensible.GetExtensionObject(bool createIfMissing)
      { return global::ProtoBuf.Extensible.GetExtensionObject(ref extensionObject, createIfMissing); }
  }
  
}