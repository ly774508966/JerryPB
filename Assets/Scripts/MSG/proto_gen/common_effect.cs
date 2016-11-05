//------------------------------------------------------------------------------
// <auto-generated>
//     This code was generated by a tool.
//
//     Changes to this file may cause incorrect behavior and will be lost if
//     the code is regenerated.
// </auto-generated>
//------------------------------------------------------------------------------

// Option: missing-value detection (*Specified/ShouldSerialize*/Reset*) enabled
    
// Generated from: common_effect.proto
namespace Common
{
  [global::System.Serializable, global::ProtoBuf.ProtoContract(Name=@"Effect")]
  public partial class Effect : global::ProtoBuf.IExtensible
  {
    public Effect() {}
    

    private Common.EffectType? _type;
    [global::ProtoBuf.ProtoMember(1, IsRequired = false, Name=@"type", DataFormat = global::ProtoBuf.DataFormat.TwosComplement)]
    public Common.EffectType type
    {
      get { return _type?? Common.EffectType.EFFECT_TYPE_INVALID; }
      set { _type = value; }
    }
    //Here has been replaced by XXMMLLDeleter
    [global::System.ComponentModel.Browsable(false)]
    public bool typeSpecified
    {
      get { return _type != null; }
      set { if (value == (_type== null)) _type = value ? type : (Common.EffectType?)null; }
    }
    private bool ShouldSerializetype() { return typeSpecified; }
    private void Resettype() { typeSpecified = false; }
    

    private float? _val;
    [global::ProtoBuf.ProtoMember(2, IsRequired = false, Name=@"val", DataFormat = global::ProtoBuf.DataFormat.FixedSize)]
    public float val
    {
      get { return _val?? default(float); }
      set { _val = value; }
    }
    //Here has been replaced by XXMMLLDeleter
    [global::System.ComponentModel.Browsable(false)]
    public bool valSpecified
    {
      get { return _val != null; }
      set { if (value == (_val== null)) _val = value ? val : (float?)null; }
    }
    private bool ShouldSerializeval() { return valSpecified; }
    private void Resetval() { valSpecified = false; }
    
    private global::ProtoBuf.IExtension extensionObject;
    global::ProtoBuf.IExtension global::ProtoBuf.IExtensible.GetExtensionObject(bool createIfMissing)
      { return global::ProtoBuf.Extensible.GetExtensionObject(ref extensionObject, createIfMissing); }
  }
  
    [global::ProtoBuf.ProtoContract(Name=@"EffectType")]
    public enum EffectType
    {
            
      [global::ProtoBuf.ProtoEnum(Name=@"EFFECT_TYPE_INVALID", Value=0)]
      EFFECT_TYPE_INVALID = 0,
            
      [global::ProtoBuf.ProtoEnum(Name=@"EFFECT_TYPE_ABSOLUTE_MAX_HP", Value=101)]
      EFFECT_TYPE_ABSOLUTE_MAX_HP = 101,
            
      [global::ProtoBuf.ProtoEnum(Name=@"EFFECT_TYPE_ABSOLUTE_CATK", Value=102)]
      EFFECT_TYPE_ABSOLUTE_CATK = 102,
            
      [global::ProtoBuf.ProtoEnum(Name=@"EFFECT_TYPE_ABSOLUTE_CDEF", Value=103)]
      EFFECT_TYPE_ABSOLUTE_CDEF = 103,
            
      [global::ProtoBuf.ProtoEnum(Name=@"EFFECT_TYPE_ABSOLUTE_SATK", Value=104)]
      EFFECT_TYPE_ABSOLUTE_SATK = 104,
            
      [global::ProtoBuf.ProtoEnum(Name=@"EFFECT_TYPE_ABSOLUTE_SDEF", Value=105)]
      EFFECT_TYPE_ABSOLUTE_SDEF = 105,
            
      [global::ProtoBuf.ProtoEnum(Name=@"EFFECT_TYPE_ABSOLUTE_CRIT", Value=106)]
      EFFECT_TYPE_ABSOLUTE_CRIT = 106,
            
      [global::ProtoBuf.ProtoEnum(Name=@"EFFECT_TYPE_ABSOLUTE_DECRIT", Value=107)]
      EFFECT_TYPE_ABSOLUTE_DECRIT = 107,
            
      [global::ProtoBuf.ProtoEnum(Name=@"EFFECT_TYPE_ABSOLUTE_INCHURT", Value=108)]
      EFFECT_TYPE_ABSOLUTE_INCHURT = 108,
            
      [global::ProtoBuf.ProtoEnum(Name=@"EFFECT_TYPE_ABSOLUTE_INHURT", Value=109)]
      EFFECT_TYPE_ABSOLUTE_INHURT = 109,
            
      [global::ProtoBuf.ProtoEnum(Name=@"EFFECT_TYPE_ABSOLUTE_DEHURT", Value=110)]
      EFFECT_TYPE_ABSOLUTE_DEHURT = 110,
            
      [global::ProtoBuf.ProtoEnum(Name=@"EFFECT_TYPE_ABSOLUTE_FORCE", Value=111)]
      EFFECT_TYPE_ABSOLUTE_FORCE = 111,
            
      [global::ProtoBuf.ProtoEnum(Name=@"EFFECT_TYPE_ABSOLUTE_INTEL", Value=112)]
      EFFECT_TYPE_ABSOLUTE_INTEL = 112
    }
  
}